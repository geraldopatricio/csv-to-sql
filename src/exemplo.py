import csv 
from SqlServer import SQLServer
import os 

def buscarNoBanco(contaDeList):
    with SQLServer() as cursor:
        #query por ordem de conta_de
        cursor.execute(f"select * from PLcontas where conta_de in ({','.join('?' * len(contaDeList))}) order by conta_de", contaDeList)
        return cursor.fetchall()

def get_conta_para(result):
    #mudar nome da coluna
    return result.conta_para

def get_conta_de(result):
    #mudar nome da coluna
    return result.conta_de
    
def get_conta_id(result):
    return result.id

def get_id_e_conta_para(contaDeId, indexRow, resultList):
    resultRow = resultList[indexRow]
    contaDeResult = get_conta_de(resultRow)
    if(contaDeResult == contaDeId):
        return get_conta_id(resultRow), get_conta_para(resultRow)

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    arq_origem_path = os.path.join(dir_path, "ArqOrigem.csv")
    arq_saida_path = os.path.join(dir_path, "ArqSaida.csv")


    with open(arq_origem_path) as file:
        csv_reader = csv.reader(file, delimiter=";")
        #pular header do arquivo e armazena para usar depois
        header = next(csv_reader)
        todas_linhas = []
        #adicionar todos os dados em um array
        for row in csv_reader:
            todas_linhas.append(row)

    #ordena as linhas csv por ordem de conta_de
    todas_linhas = sorted(todas_linhas, key=lambda row: row[0])

    #separa o id de cada linha para buscar no banco
    contaDeList = [item[0] for item in todas_linhas]

    #busca os registros no banco para cada um dos conta_de
    resultList = buscarNoBanco(contaDeList)

    #busca index of ContaDe no csv
    index_of_conta_de = header.index("ContaDe")

    #usa o index e a propria linha. Como ambos estão ordenados(csv e banco) por ordem de conta_de basta juntar as duas informações
    for index, row in enumerate(todas_linhas):
        contaDe = row[index_of_conta_de]
        id, contaPara = get_id_e_conta_para(contaDeId=contaDe, indexRow=index, resultList=resultList)
        row[index_of_conta_de] = contaPara
        row.insert(0, id)

    #Adiciona Conta no fim do Header
    header[index_of_conta_de] = ("Conta")
    header.insert(0, "id")

    #escreve as informaçoes no csv
    with open(arq_saida_path, "w") as file_w:
        csv_writer = csv.writer(file_w, delimiter=";")
        csv_writer.writerow(header)
        csv_writer.writerows(todas_linhas)

        

