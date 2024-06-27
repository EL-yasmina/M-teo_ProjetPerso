import pytest
from unittest.mock import patch
from app.api.v1.alert import recommandation_vetements, previsions_meteo, infos_ville, qualite_air, previsions_horaires

def test_recommandation_vetements_froid(mocker):
    mock_response = {
        'location': {'name': 'Paris'},
        'current': {
            'temp_c': 5,
            'condition': {'text': 'Sunny'},
            'precip_mm': 0
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    expected_result = "Il fait plutôt frais à Paris avec 5°C. Tu devrais peut-être envisager de porter quelque chose de chaud !"
    assert recommandation_vetements('Paris') == expected_result


def test_recommandation_vetements_printemps_avec_pluie(mocker):
    mock_response = {
        'location': {'name': 'Lyon'},
        'current': {
            'temp_c': 15,
            'condition': {'text': 'Rain'},
            'precip_mm': 5
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    expected_result = "Il y a Rain à Lyon et il fait 15°C. Prends un parapluie et peut-être un pull léger !"
    assert recommandation_vetements('Lyon') == expected_result


def test_recommandation_vetements_printemps_sans_pluie(mocker):
    mock_response = {
        'location': {'name': 'Marseille'},
        'current': {
            'temp_c': 18,
            'condition': {'text': 'Cloudy'},
            'precip_mm': 0
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    expected_result = "À Marseille il fait 18°C, un t-shirt et une veste légère pourraient être parfaits pour toi !"
    assert recommandation_vetements('Marseille') == expected_result


def test_recommandation_vetements_chaud_avec_pluie(mocker):
    mock_response = {
        'location': {'name': 'Nice'},
        'current': {
            'temp_c': 25,
            'condition': {'text': 'Rain'},
            'precip_mm': 10
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    expected_result = "Il pleut à Nice et il fait 25°C. N'oublie pas ton parapluie !"
    assert recommandation_vetements('Nice') == expected_result


def test_recommandation_vetements_chaud_sans_pluie(mocker):
    mock_response = {
        'location': {'name': 'Toulouse'},
        'current': {
            'temp_c': 30,
            'condition': {'text': 'Sunny'},
            'precip_mm': 0
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    expected_result = "Il fait chaud à Toulouse avec 30°C. C'est le moment de sortir les shorts et les lunettes de soleil !"
    assert recommandation_vetements('Toulouse') == expected_result


def test_recommandation_vetements_requete_echoue(mocker):
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 404

    assert recommandation_vetements('InvalidCity') is None


def test_previsions_meteo(mocker):
    city = "Paris"
    days = 3
    mock_response = {
        'forecast': {
            'forecastday': [
                {'date': '2024-06-27', 'day': {'maxtemp_c': 25, 'mintemp_c': 15, 'condition': {'text': 'Sunny'}}},
                {'date': '2024-06-28', 'day': {'maxtemp_c': 28, 'mintemp_c': 18, 'condition': {'text': 'Cloudy'}}},
                {'date': '2024-06-29', 'day': {'maxtemp_c': 22, 'mintemp_c': 14, 'condition': {'text': 'Rainy'}}}
            ]
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    result = previsions_meteo(city, days)
    assert len(result) == 3
    assert result[0]['date'] == '2024-06-27'


def test_infos_ville(mocker):
    city = "Paris"
    mock_response = {
        'location': {'name': 'Paris', 'region': 'Ile-de-France', 'country': 'France'}
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    result = infos_ville(city)
    assert result['name'] == 'Paris'
    assert result['region'] == 'Ile-de-France'
    assert result['country'] == 'France'


def test_qualite_air(mocker):
    city = "Paris"
    mock_response = {
        'current': {
            'air_quality': {
                'pm2_5': 12.0,
                'pm10': 20.0
            }
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    result = qualite_air(city)
    assert result['pm2_5'] == 12.0
    assert result['pm10'] == 20.0


def test_previsions_horaires(mocker):
    city = "Paris"
    mock_response = {
        'forecast': {
            'forecastday': [{
                'hour': [{'time': '2024-06-27 00:00', 'temp_c': 15, 'condition': {'text': 'Clear'}}]
            }]
        }
    }
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = mock_response

    result = previsions_horaires(city)
    assert len(result) == 1
    assert result[0]['time'] == '2024-06-27 00:00'
    assert result[0]['temp_c'] == 15
