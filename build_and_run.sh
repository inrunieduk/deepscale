echo "###   Construindo imagem Docker   ###"
docker build -t deepscale .
echo $'\n'

echo "###   Inicializando imagem Docker   ###"
docker run -it -p 5000:5000 deepscale