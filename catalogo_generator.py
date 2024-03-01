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
    "variables": "{\"input\":[{\"context\":\"OFFER\",\"query\":\"grátis\",\"limit\":20,\"sort\":{\"by\":\"createdAt\"}},{\"context\":\"PRODUCT\",\"query\":\"grátis\",\"limit\":20},{\"context\":\"STORE\",\"query\":\"grátis\",\"limit\":20}]}"
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
        f.write('.card { height: 100%; }\n')
        f.write('.card-img-top { max-width: 100%; height: auto; }\n')
        f.write('.card-title { font-size: 1.2rem; }\n')  # Define o tamanho do texto do título
        f.write('.card-body { display: flex; flex-direction: column; justify-content: space-between; }\n')  # Ajusta o layout do card body
        f.write('.btn-primary { width: 100%; }\n')  # Define o botão com largura de 100%
        f.write('</style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<div class="container">\n')

        count = 0
        for item in data['data']['public']['federatedSearchV1']['searches']:
            for edge in item['edges']:
                if count % 4 == 0:
                    f.write('<div class="row row-cols-1 row-cols-md-4 g-4 mb-4">\n')

                image_url = edge['image']['url']
                source_url = edge['sourceUrl']
                title = edge['title']
                
                f.write('<div class="col">\n')
                f.write('<div class="card h-100">\n')
                f.write(f'<img src="{image_url}" class="card-img-top" alt="Imagem" style="width: 300px; height: 300px; object-fit: cover;" crossorigin="anonymous">\n')
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
