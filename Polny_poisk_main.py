import os
import sys
import pygame
import requests
from get_spn import get_spn

geocode = input('Введите адрес: ')
api_key = "8013b162-6b42-4997-9691-77b7074026e0"
server_address = 'http://geocode-maps.yandex.ru/1.x/?'
geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'
response = requests.get(geocoder_request)

if response:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_coodrinates = toponym_coodrinates.replace(' ', ',')
else:
    print('Неверный запрос')
    sys.exit(0)

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = toponym_coodrinates
x = float(address_ll.split(',')[0])
y = float(address_ll.split(',')[1])
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print('Неверный запрос')
    sys.exit(0)

json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
print('Ближайшая аптека:', org_name, org_address)

point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
spn_x, spn_y = get_spn([x, y], point)

apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
map_params = {
    "ll": address_ll,
    "spn": ",".join([str(spn_y), str(spn_x)]),
    "apikey": apikey,
    "pt": "{0},pmrds".format(org_point)
}
map_api_server = "https://static-maps.yandex.ru/v1"
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"

with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
pygame.display.set_caption('Ближайшая аптека')
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
font = pygame.font.Font(None, 30)
show_x = org_point.split(',')[1]
show_y = org_point.split(',')[0]
string_rendered = font.render(show_x + ', ' + show_y, 1, pygame.Color('black'))
text_rect = string_rendered.get_rect()
text_rect.top = 430
text_rect.x = 10
screen.blit(string_rendered, text_rect)
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)