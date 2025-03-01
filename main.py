from models import create_tables, Publisher, Book, Shop, Stock, Sale
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json


def read_json(file_name):
    with open(file_name, encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data


def insert_from_json(file_name):
    data = read_json(file_name)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def found_sales(param):
    que = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock).
            join(Stock.book).join(Stock.shop).
            join(Book.publisher))

    if param.isdigit():
        que = que.filter(Publisher.id == param).all()
    else:
        que = que.filter(Publisher.name == param).all()
    if not param:
        print('Не введены требуемые данные!')
        return
    if que:
        for c in que:
            print(f'{c[0]}{" " * (60 - len(c[0]))} | '
                  f'{c[1]}{" " * (10 - len(c[1]))} | '
                  f'{c[2]}{" " * (6 - len(str(c[2])))} | '
                  f'{c[3]}')
    else:
        print("У данного автора нет проданных книг")
        return


if __name__ == '__main__':
    params = read_json('params.json')[0]
    DSN = (f"postgresql://{params.get('user')}:{params.get('password')}@"
           f"{params.get('host')}:{params.get('port')}/{params.get('db_name')}")
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    insert_from_json('tests_data.json')
    found_sales(input('Введите имя или id автора: '))1