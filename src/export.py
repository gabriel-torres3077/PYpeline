import utils
import csv
import os
import pandas as pd

collection = utils.collection
BASE_DIR = f'{os.getcwd()}\src'
STATS_PATH =  f'{BASE_DIR}\estatisticas'

def get_ativos():
    total_entries = collection.count_documents({})
    actives = collection.count_documents({"SITUAÇÃO_CADASTRAL": "02"})
    active_users = round(((actives * 100) / total_entries), 2)
    return active_users

def list_restaurants():
    pipeline = [
        {"$match": {
            "CNAE_PRINCIPAL": {"$regex": "^561"}
            }
        },
        {"$group": {
            "_id": {"$year": {"$dateFromString": {"dateString": "$DATA_INÍCIO", "format": "%Y%m%d"}}},
            "count": {"$sum": 1}
            }
        }
    ]
    restaurants = list(collection.aggregate(pipeline))
    return restaurants

def main():

    actives = get_ativos()
    restaurants = list_restaurants()
    # Write cnpj
    with open(f'{STATS_PATH}\CNPJ_ativos.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['CNPJ ATIVOS'])
        writer.writerow([actives])
        f.close()
    
    # Write List
    restaurant_fields = {'_id': 'Ano', 'count': 'Quantidade de restaurantes abertos'}
    with open(f'{STATS_PATH}\Restaurantes_por_ano.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=restaurant_fields)
        writer.writerow(restaurant_fields)
        writer.writerows(restaurants)
        f.close()

    #export to excel
    csv1 = pd.read_csv(f'{STATS_PATH}\CNPJ_ativos.csv')
    csv2 = pd.read_csv(f'{STATS_PATH}\Restaurantes_por_ano.csv')

    with pd.ExcelWriter(f'{STATS_PATH}\estatisticas.xlsx') as writer:
        csv1.to_excel(writer, sheet_name='CNPJ ativos')
        csv2.to_excel(writer, sheet_name='Restaurantes abertos por ano')




if __name__ == '__main__':
    if not os.path.exists(STATS_PATH):
        os.makedirs(STATS_PATH)
    main()
