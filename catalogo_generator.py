import os
import json
import requests

# Verifica se o arquivo HTML existe e o exclui, se existir
if os.path.exists('catalogo.html'):
    os.remove('catalogo.html')

# Restante do código permanece o mesmo
url = "https://www.pelando.com.br/api/graphql"
querystring = {
    "query": "query FederatedSearch($input:[federatedSearchV1Input!]!){public{federatedSearchV1(input:$input){rules{mainContext}searches{...FederatedSearchReturnOffersFragment...FederatedSearchReturnProductsFragment...FederatedSearchReturnStoresFragment...FederatedSearchReturnSuggestionsFragment}}}}fragment FacetsFragment on Facet{type field name options{...RangeFacetOptionFragment...TextFacetOptionFragment}}fragment TextFacetOptionFragment on TextFacetOption{values{count value}}fragment RangeFacetOptionFragment on RangeFacetOption{from to}fragment FederatedSearchReturnOffersFragment on FederatedSearchV1ReturnOffers{searchId context edges{id discountFixed discountPercentage freeShipping image{id url(height:238)}price sourceUrl status temperature kind isTracked couponCode commentCount timestamps{...DealTimestampsFragment}title store{name slug url image{id url(height:238)}}}pageInfo{...PageInfoFragment}facets{...FacetsFragment}total}fragment FederatedSearchReturnProductsFragment on FederatedSearchV1ReturnProducts{searchId indexSource context edges{id title categoryId image{id url}indexSource currentMinPrice totalStoresCount minPriceStore{name}rangePercentageMessage{status}}pageInfo{...PageInfoFragment}facets{...FacetsFragment}total}fragment FederatedSearchReturnStoresFragment on FederatedSearchV1ReturnStores{searchId context edges{id name slug couponsCount offersCount productsCount image{id url(width:64)}}pageInfo{hasNextPage endCursor}total}fragment FederatedSearchReturnSuggestionsFragment on FederatedSearchV1ReturnSuggestions{context edges{suggestion}}fragment DealTimestampsFragment on OfferTimestamps{firstApprovedAt approvedAt createdAt pickedAt lastCommentedAt publishAt}fragment PageInfoFragment on PageInfo{startCursor endCursor hasNextPage hasPreviousPage}",
    "variables": "{\"input\":[{\"context\":\"OFFER\",\"query\":\"grátis\",\"sort\":{\"by\":\"createdAt\"}},{\"context\":\"PRODUCT\",\"query\":\"grátis\"},{\"context\":\"STORE\",\"query\":\"grátis\"}]}"
}

response = requests.get(url, params=querystring)

if response.status_code == 200:
    data = response.json()

    with open('catalogo.html', 'w') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<title>Catálogo</title>\n')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
        f.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"  rel="stylesheet">\n')
        f.write('<style>\n')
        f.write('.card { height: 100%; background-color: rgb(34, 34, 34, 0.8); border: 1px solid #ccc; padding: 10px; }\n')  # Define a cor de fundo e a borda do card com o RGB fornecido
        f.write('.card-img-top { width: 150px; height: 150px; object-fit: cover; margin: auto; margin-bottom: 10px; border-radius: 4px; }\n')  # Define o tamanho, centraliza a imagem e adiciona borda
        f.write('.card-title { font-size: 1.2rem; color: white; }\n')  # Define o tamanho e a cor do texto do título do card
        f.write('.card-body { display: flex; flex-direction: column; justify-content: space-between; }\n')  # Ajusta o layout do card body
        f.write('.btn-primary { width: 100%; background-color: rgb(167, 139, 250, 0.8); border-color: rgb(167, 139, 250, 0.8); }\n')  # Define a cor do botão com o RGB fornecido
        f.write('.btn-primary:hover { background-color: rgb(167, 139, 250); border-color: rgb(167, 139, 250); }\n')  # Define a cor do botão ao passar o mouse
        f.write('body { background-color: rgb(21, 21, 21); }\n')  # Define o background com o RGB fornecido
        f.write('.navbar { position: fixed; top: 0; width: 100%; z-index: 1000; }\n')  # Deixa o menu fixo no topo
        f.write('.navbar-brand { margin-right: 2rem; }\n')  # Define o espaçamento à direita para o logo
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<nav class="navbar navbar-expand-lg navbar-dark bg-dark">\n')
        f.write('<div class="container">\n')
        f.write('<a class="navbar-brand" href="#">QueroGrátis</a>\n')
        f.write('</div>\n')
        f.write('</nav>\n')
        f.write('<div class="container" id="card-container">\n')

        count = 0
        for item in data['data']['public']['federatedSearchV1']['searches']:
            for edge in item['edges']:
                title = edge['title']
                f.write(f'<h5 style="display: none;">{title}</h5>\n')

                if count % 4 == 0:
                    f.write('<div class="row row-cols-1 row-cols-md-4 g-4 mb-4">\n')

                image_url = edge['image']['url']
                source_url = edge['sourceUrl']
                title = edge['title']
                
                f.write('<div class="col">\n')
                f.write('<div class="card">\n')  # Removido 'h-100' para permitir o ajuste automático do tamanho do card
                f.write(f'<img src="{image_url}" class="card-img-top" alt="Imagem" crossorigin="anonymous">\n')  # Removido o estilo width e height para usar as dimensões padrão da imagem
                f.write('<div class="card-body">\n')
                f.write(f'<h5 class="card-title">{title}</h5>\n')
                f.write(f'<a href="{source_url}" class="btn btn-primary stretched-link align-self-center" target="_blank">Ver Detalhes</a>\n')  # Alinha o botão ao centro verticalmente
                f.write('</div>\n')
                f.write('</div>\n')
                f.write('</div>\n')

                if count % 4 == 3:
                    f.write('</div>\n')

                count += 1

        f.write('</div>\n')
        f.write('</body>\n')
        f.write('</html>\n')

    print("Catálogo HTML gerado com sucesso!")
else:
    print("Falha ao obter dados. Status code:", response.status_code)
