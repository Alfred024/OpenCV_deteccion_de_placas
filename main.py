# pip install requests
import requests
# urlDemo = "https://jsonplaceholder.typicode.com/photos";

placa = "JU45393"
url = "/api/reg.asmx/CheckMexico?RegistrationNumber=string&username=Alfredo_JimenezT"

headers = {
	"Authorization": "a950074d08eab7d5de00fc38e0eb15bd7ed8ca54",
	"X-RapidAPI-Key": "eeffe32181msh7e526b10e078b85p19a463jsndf6b1291f329",
	"X-RapidAPI-Host": "informacion-vehiculos-de-mexico.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
#response = requests.get(urlDemo)

print('Respuesta petición: ')
print(response)
