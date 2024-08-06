import hashlib
import json
import random
import time
import datetime
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request, render_template, json


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, id_peqprod, id_fazenda, id_vaca, id_tanque, volume_ordenhado, base_date):
        self.current_transactions.append({
            'id_peqprod': id_peqprod,
            'id_fazenda': id_fazenda,
            'id_vaca': id_vaca,
            'id_tanque': id_tanque,
            'volume_ordenhado': volume_ordenhado,
            'base_date': base_date
        })

        return self.last_block['index'] + 1

    def new_transaction_2(self, id_caminhao, id_e_t, id_r_t, o_armazenamento_tprt, o_armazenamento_temp, analise1,
                          volume_at1, tempo_armazenado, data_transporte):

        seconds = time.time()
        self.current_transactions.append({
            'id_r_t': id_r_t,
            'id_e_t': id_e_t,
            'id_caminhao': id_caminhao,
            'o_armazenamento_tprt': o_armazenamento_tprt,
            'o_armazenamento_temp': o_armazenamento_temp,
            'analise1': analise1,
            'volume_at1': volume_at1,
            'tempo_armazenado': tempo_armazenado,
            'data_transporte': data_transporte
        })

        return self.last_block['index'] + 1

    def new_transaction_3(self, analise2, volume_fabrica, data_trans, past, data_past, analise_lc, data_lc, id_lote,
                          est, data_est):

        seconds = time.time()
        self.current_transactions.append({
            'analise2': analise2,
            'volume_fabrica': volume_fabrica,
            'data_trans': data_trans,
            'past': past,
            'data_past': data_past,
            'analise_lc': analise_lc,
            'data_lc': data_lc,
            'id_lote': id_lote,
            'est': est,
            'data_est': data_est
        })

        return self.last_block['index'] + 1

    def new_transaction_4(self, id_lote, pallets, id_centro_distribuicao1):

        seconds = time.time()
        self.current_transactions.append({
            'id_lote': id_lote,
            'pallets': pallets,
            'id_centro_distribuicao1': id_centro_distribuicao1
        })

        return self.last_block['index'] + 1

    def new_transaction_5(self, ids_pallets_caminhao, id_caminhao, id_emp_log, id_respp_ent, data_saida_caminhao,
                          id_centro_distribuicao2):

        seconds = time.time()
        self.current_transactions.append({
            'ids_pallets_caminhao': ids_pallets_caminhao,
            'id_caminhao': id_caminhao,
            'id_emp_log': id_emp_log,
            'id_respp_ent': id_respp_ent,
            'data_saida_caminhao': data_saida_caminhao,
            'id_centro_distribuicao2': id_centro_distribuicao2
        })

        return self.last_block['index'] + 1

    def new_transaction_6(self, id_mercado, id_resp_merc, id_caminhao2, id_respp_ent2, id_empr_log2, pallets_entregues,
                          data_entrega):

        seconds = time.time()
        self.current_transactions.append({
            'id_mercado': id_mercado,
            'id_resp_merc': id_resp_merc,
            'id_caminhao2': id_caminhao2,
            'id_respp_ent2': id_respp_ent2,
            'id_empr_log2': id_empr_log2,
            'pallets_entregues': pallets_entregues,
            'data_entrega': data_entrega
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @property
    def penultimate_block(self):
        return self.chain[-2]

    @property
    def get_equivalent_block(self):
        return self.chain[-6]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    @property
    def random_signal(self):
        z = random.random()
        y = 0
        if z < 0.95:
            y = 1
        else:
            pass
        return y

    @property
    def calculo_v_o(self):
        y = random.randrange(500, 550)
        return y

    @property
    def calculo_t_leite(self):
        y = random.randrange(24, 50)
        return y

    @property
    def numero_de_quatro_digitos(self):
        numero_de_quatro_digitos = []
        for i in range(0, 4):
            i = random.randrange(0, 9)
            numero_de_quatro_digitos.append(i)
            y = ''.join([str(numero) for numero in numero_de_quatro_digitos])
        return y

    @property
    def caixas_de_um_litro(self):
        caixa = []
        numero_de_quatro_digitos = []
        qq = 0
        for j in range(1, 12):
            if len(caixa) == 0:
                for i in range(0, 4):
                    i = random.randrange(0, 9)
                    numero_de_quatro_digitos.append(i)
                    y = (''.join([str(numero) for numero in numero_de_quatro_digitos]))
                    if len(y) == 4:
                        y = int(y)
                        caixa.append(y)
                    else:
                        pass
                    qq += 1
            else:
                pass
            y = int(y)
            y += 1
            caixa.append(y)
        return caixa

    @property
    def gen_timestamp(self, min_year=2019, max_year=2030):
        # gera um datetime no formato yyyy-mm-dd hh:mm:ss.000000
        year = random.randint(min_year, max_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(5, 12)
        minute = random.randint(1, 59)
        second = random.randint(1, 59)
        microsecond = random.randint(1, 999999)
        date = datetime.datetime(
            year, month, day, hour, minute, second, microsecond).isoformat(" ")
        return date

    def sum_timestamp(self, date_1, t_leite_horas, t_leite_dias):
        days = t_leite_dias
        hours = t_leite_horas
        new_date = date_1 + datetime.timedelta(days=days, hours=hours)
        return new_date


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # como tem diversos ifs e elses talve um fluxograma ajude na compreensao
    for k in range(0, 50):
        if last_block['index'] + 1 == 2 + 6 * k:
            # ORDENHA

            # IDs
            # Id pequeno produtor - x1
            # Id fazenda - x2
            # Id tanque - x4
            x1 = blockchain.numero_de_quatro_digitos
            x2 = blockchain.numero_de_quatro_digitos
            x4 = blockchain.numero_de_quatro_digitos

            # Lista de ids das vacas
            ids_vacas = []
            for i in range(0, 100):
                x3 = blockchain.numero_de_quatro_digitos
                ids_vacas.append(x3)
            ids_vacas_sem_duplicatas = list(set(ids_vacas))

            # Eliminacao de duplicatas de lista de ids das vacas
            for i in range(0, 50):
                if len(ids_vacas_sem_duplicatas) <= 99:
                    i = blockchain.numero_de_quatro_digitos
                    ids_vacas_sem_duplicatas.append(i)
                    ids_vacas_sem_duplicatas = list(set(ids_vacas_sem_duplicatas))
                else:
                    pass

            # Volume Ordenhado
            v_o = blockchain.calculo_v_o

            # Timestamp ordenha
            if k == 0:
                base_date = blockchain.gen_timestamp
            else:
                ab = blockchain.get_equivalent_block['transactions']
                ab = ab[0]
                date_a = ab['base_date']
                date_a = datetime.datetime.strptime(date_a, '%Y-%m-%d %H:%M:%S.%f')
                data_aa = date_a + datetime.timedelta(days=1, seconds=1, microseconds=1, milliseconds=1, weeks=1)
                base_date = data_aa.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Cria uma transacao referente a etapa de ordenha
            blockchain.new_transaction(
                id_peqprod=x1,
                id_fazenda=x2,
                id_vaca=ids_vacas_sem_duplicatas,
                id_tanque=x4,
                volume_ordenhado=v_o,
                base_date=base_date
            )


        elif last_block['index'] + 1 == 3 + 6 * k:
            # TRANSPORTE

            # IDs
            x5 = blockchain.numero_de_quatro_digitos
            x6 = blockchain.numero_de_quatro_digitos
            x7 = blockchain.numero_de_quatro_digitos

            # Volume
            abb = last_block['transactions']
            abb = abb[0]
            abb = abb['volume_ordenhado']
            v_at1 = blockchain.random_signal
            if v_at1 == 1:
                v_at1 = abb
            else:
                v_at1 = 0.85 * abb

            # Tempo de armazenamento do leite
            t_leite = blockchain.calculo_t_leite
            t_leite_horas = (t_leite % 24)
            t_leite_dias = (t_leite // 24)

            # Respeitou limite de tempo?
            o_a_temp = 'Sim'
            if t_leite > 48:
                o_a_temp = 'Não'
            else:
                pass

            # Respeitou limite de temperatura?
            o_a = blockchain.random_signal
            if o_a == 1:
                o_a2 = 'Sim'
            else:
                o_a2 = 'Não'

            # Analise de qualidade I
            a_q = blockchain.random_signal
            if a_q == 1:
                a_q2 = ' Normal'
            else:
                a_q2 = ' Lina'

            # Timestamp transporte
            abb1 = last_block['transactions']
            abb1 = abb1[0]
            date_1 = abb1['base_date']
            date_1 = datetime.datetime.strptime(date_1, '%Y-%m-%d %H:%M:%S.%f')
            data_transporte = blockchain.sum_timestamp(date_1, t_leite_horas, t_leite_dias)
            data_transporte = data_transporte.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Transforma tempo de armazenamento do leite em string
            t_leite_horas = str(t_leite_horas)
            t_leite_dias = str(t_leite_dias)

            # Cria uma transacao referente a etapa de transporte
            blockchain.new_transaction_2(
                o_armazenamento_temp='O armazenamento respeitou os limites de tempo?  ' + o_a_temp,
                o_armazenamento_tprt='O armazenamento respeitou os limites de temperatura?  ' + o_a2,
                id_caminhao=x5,
                id_e_t=x6,
                id_r_t=x7,
                analise1='Analise de qualidade do leite I - ' + a_q2,
                volume_at1=v_at1,
                tempo_armazenado='Armazenado a ' + t_leite_dias + ' dia(s) e  ' + t_leite_horas + ' hora(s)',
                data_transporte=data_transporte
            )


        elif last_block['index'] + 1 == 4 + 6 * k:
            # Fabrica

            # Analise de qualidade II
            a_qii = blockchain.random_signal
            if a_qii == 1:
                a_qii2 = ' Normal'
            else:
                a_qii2 = ' Lina'

            # Volume ao chegar na fabrica
            abc = last_block['transactions']
            abc = abc[0]
            abc = abc['volume_at1']
            v_f = blockchain.random_signal
            if v_f == 1:
                v_f = abc
            else:
                v_f = 0.85 * abc

            # Timestamp de chegada na fabrica
            t_trans_horas = random.randrange(2, 5)
            t_trans_minutos = random.randrange(0, 59)
            abc1 = last_block['transactions']
            abc1 = abc1[0]
            date_2 = abc1['data_transporte']
            date_2 = datetime.datetime.strptime(date_2, '%Y-%m-%d %H:%M:%S.%f')
            data_trans = date_2 + datetime.timedelta(minutes=t_trans_minutos, hours=t_trans_horas)
            data_trans = data_trans.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Pasteurizacao
            a_p = blockchain.random_signal
            if a_p == 1:
                a_p2 = ' Sim'
            else:
                a_p2 = ' Não'

            # Timestamp Pasteurizacao
            data_sl = datetime.datetime.strptime(data_trans, '%Y-%m-%d %H:%M:%S.%f')
            data_past = data_sl + datetime.timedelta(hours=3)
            data_past = data_past.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Analise de laboratorio central
            a_lc = blockchain.random_signal
            if a_lc == 1:
                a_lc2 = ' Ok'
            else:
                a_lc2 = ' Recusado'

            # Timestamp Analise de laboratorio central
            data_sl2 = datetime.datetime.strptime(data_past, '%Y-%m-%d %H:%M:%S.%f')
            data_lc = data_sl2 + datetime.timedelta(hours=1, minutes=30)
            data_lc = data_lc.strftime('%Y-%m-%d %H:%M:%S.%f')

            # IDs
            x8 = blockchain.numero_de_quatro_digitos

            # Esterilizacao
            a_e = blockchain.random_signal
            if a_e == 1:
                a_e2 = ' Sim'
            else:
                a_e2 = ' Não'

            # Timestamp Esterilizacao
            data_sl3 = datetime.datetime.strptime(data_lc, '%Y-%m-%d %H:%M:%S.%f')
            data_est = data_sl3 + datetime.timedelta(minutes=30)
            data_est = data_est.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Cria uma transacao referente a etapa Fabrica
            blockchain.new_transaction_3(
                analise2='Analise de qualidade do leite II - ' + a_qii2,
                volume_fabrica=v_f,
                data_trans=data_trans,
                past='Pasteurizacao completa?  ' + a_p2,
                data_past=data_past,
                analise_lc=a_lc2,
                data_lc=data_lc,
                id_lote=x8,
                est='Esterilizacao completa?  ' + a_e2,
                data_est=data_est
            )


        elif last_block['index'] + 1 == 5 + 6 * k:
            # TRANSFERENCIA DE CAIXA DE LEITE

            # x9 = id lote
            # x10 = id centro de distribuicao
            # IDC = Id do Caminhão
            abd = last_block['transactions']
            abd = abd[0]
            x9 = abd['id_lote']
            x10 = blockchain.numero_de_quatro_digitos

            # Cria e organiza as IDs das caixas de 1 litro, das caixas grandes e dos pallets
            pallets = {}
            z = int(blockchain.numero_de_quatro_digitos)
            for tantof in range(0, 26):
                z += 1
                pallet = {}
                y = int(blockchain.numero_de_quatro_digitos)
                for x in range(1, 22):
                    y += 1
                    caixa_grande = blockchain.caixas_de_um_litro
                    pallet["Caixa Grande {0}".format(str(y))] = caixa_grande
                pallets["Pallet {0}".format(str(z))] = pallet

            # Cria uma transacao referente a etapa Transferencia para caixa de leite
            blockchain.new_transaction_4(
                id_lote=x9,
                pallets=pallets,
                id_centro_distribuicao1=x10
            )


        elif last_block['index'] + 1 == 6 + 6 * k:
            # Logistica parte I

            # id_el - id empresa de logistica
            # idc - id caminhao
            # id_rpe - id responsavel pela entrega
            # id_cdd - id centro de distribuicao
            id_el = blockchain.numero_de_quatro_digitos
            idc = blockchain.numero_de_quatro_digitos
            id_rpe = blockchain.numero_de_quatro_digitos
            abe = last_block['transactions']
            abe = abe[0]
            abe = abe['id_centro_distribuicao1']
            id_cdd = abe

            # lista com ids dos pallets que se encontram dentro do caminhão
            abe1 = last_block['transactions']
            abe1 = abe1[0]
            abe1 = abe1['pallets']
            lp = list(abe1.keys())

            # Timestamp chegada do caminhao
            t_chegc_horas = random.randrange(10, 50)
            t_chegc_minutos = random.randrange(0, 59)
            abe2 = blockchain.penultimate_block['transactions']
            abe2 = abe2[0]
            date_3 = abe2['data_lc']
            date_3 = datetime.datetime.strptime(date_3, '%Y-%m-%d %H:%M:%S.%f')
            data_trans_3 = blockchain.sum_timestamp(date_3, t_chegc_horas, t_chegc_minutos)
            data_trans_3 = data_trans_3.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Cria uma transacao referente a etapa Logistica I
            blockchain.new_transaction_5(
                ids_pallets_caminhao=lp,
                id_caminhao=idc,
                id_emp_log=id_el,
                id_respp_ent=id_rpe,
                data_saida_caminhao=data_trans_3,
                id_centro_distribuicao2=id_cdd
            )


        elif last_block['index'] + 1 == 7 + 6 * k:
            # Logistica parte II

            # id_merc - id do mercado que recebe os pallets
            # id_r_merc - id do responsavel do mercado que recebe os pallets
            id_merc = blockchain.numero_de_quatro_digitos
            id_r_merc = blockchain.numero_de_quatro_digitos

            # id caminhao
            abf = last_block['transactions']
            abf = abf[0]
            abf = abf['id_caminhao']
            idc2 = abf

            # id responsavel pela entrega
            abf1 = last_block['transactions']
            abf1 = abf1[0]
            abf1 = abf1['id_respp_ent']
            id_rpe2 = abf1

            # id empresa de logistica
            abf2 = last_block['transactions']
            abf2 = abf2[0]
            abf2 = abf2['id_emp_log']
            id_el2 = abf2

            # lista com ids dos pallets que se encontram dentro do caminhão
            abf3 = last_block['transactions']
            abf3 = abf3[0]
            abf3 = abf3['ids_pallets_caminhao']
            n = 3
            pmcd = abf3[slice(n)]

            # # Timestamp transporte
            t_cheg_merc_horas = random.randrange(1, 10)
            t_cheg_merc_minutos = random.randrange(0, 59)
            abf4 = last_block['transactions']
            abf4 = abf4[0]
            date_4 = abf4['data_saida_caminhao']
            date_4 = datetime.datetime.strptime(date_4, '%Y-%m-%d %H:%M:%S.%f')
            data_trans_4 = blockchain.sum_timestamp(date_4, t_cheg_merc_horas, t_cheg_merc_minutos)
            data_trans_4 = data_trans_4.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Cria uma transacao referente a etapa Logistica II
            blockchain.new_transaction_6(
                id_mercado=id_merc,
                id_resp_merc=id_r_merc,
                id_caminhao2=idc2,
                id_respp_ent2=id_rpe2,
                id_empr_log2=id_el2,
                pallets_entregues=pmcd,
                data_entrega=data_trans_4
            )

        else:
            pass

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    html_item_1 = json.dumps(response, indent=2, separators=(',', ':'))

    return render_template("./mine.html", html_item_1=html_item_1)


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    if last_block['index'] + 1 == 2:
        # Check that the required fields are in the POST'ed data
        required = ['id_peqprod', 'id_fazenda', 'id_vaca' 'id_tanque', 'volume_ordenhado', 'base_date']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['id_peqprod'], values['id_fazenda'], values['id_vaca'],
                                           values['id_tanque'], values['volume_ordenhado'], values['base_date'])

        response = {'message': f'Transaction will be added to Block {index}'}

    elif last_block['index'] + 1 == 3:
        # Check that the required fields are in the POST'ed data
        required = ['id_e_t', 'id_r_t', 'id_caminhao', 'o_armazenamento_tprt', 'o_armazenamento_temp', 'analise1',
                    'volume_at1', 'tempo_armazenado', 'data_transporte']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['id_e_t'], values['id_r_t'], values['id_caminhao'],
                                           values['o_armazenamento_tprt'], values['o_armazenamento_temp'],
                                           values['analise1'], values['volume_at1'], values['tempo_armazenado'],
                                           values['data_transporte'])

        response = {'message': f'Transaction will be added to Block {index}'}

    elif last_block['index'] + 1 == 4:
        # Check that the required fields are in the POST'ed data
        required = ['analise2', 'volume_fabrica', 'data_trans', 'past', 'data_past', 'analise_lc', 'data_lc', 'id_lote',
                    'est', 'data_est']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['analise2'], values['volume_fabrica'], values['data_trans'],
                                           values['past'], values['data_past'], values['analise_lc'], values['data_lc'],
                                           values['id_lote'], values['est'], values['data_est'])

        response = {'message': f'Transaction will be added to Block {index}'}

    elif last_block['index'] + 1 == 5:
        # Check that the required fields are in the POST'ed data
        required = ['id_lote', 'pallets', 'id_centro_distribuicao1']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['id_lote'], values['pallets'], values['id_centro_distribuicao1'])

        response = {'message': f'Transaction will be added to Block {index}'}

    elif last_block['index'] + 1 == 6:
        # Check that the required fields are in the POST'ed data
        required = ['ids_pallets_caminhao', 'id_caminhao', 'id_emp_log', 'id_respp_ent', 'data_saida_caminhao',
                    'id_centro_distribuicao2']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['ids_pallets_caminhao'], values['id_caminhao'], values['id_emp_log'],
                                           values['id_respp_ent'], values['data_saida_caminhao'],
                                           values['id_centro_distribuicao2'])

        response = {'message': f'Transaction will be added to Block {index}'}

    elif last_block['index'] + 1 == 7:
        # Check that the required fields are in the POST'ed data
        required = ['id_mercado', 'id_resp_merc', 'id_caminhao2', 'id_respp_ent2', 'id_empr_log2', 'pallets_entregues',
                    'data_entrega']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['id_mercado'], values['id_resp_merc'], values['id_caminhao2'],
                                           values['id_respp_ent2'], values['id_empr_log2'], values['pallets_entregues'],
                                           values['data_entrega'])

        response = {'message': f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    html_item_2 = json.dumps(response, indent=2, separators=(',', ':'))
    return render_template("./chain.html", html_item_2=html_item_2)


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
