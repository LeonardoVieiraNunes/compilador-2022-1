#INE5426 - Construção de Compiladores - Analisador Léxico, Sintático, Semântico e GCI
# Artur Ribeiro Alfa [17103919]
# Augusto Vieira Coelho Rodrigues [19100517]
# Leonardo Vieira Nunes [19102923]
# Thainan Vieira Junckes [19100545]

from itertools import combinations
from dataclasses import dataclass
from typing import List, Union, Set, Tuple, Dict

from utils.data_structures import Cfg, Production, SyntaticAnalyserMatrix
from utils.cfg_parser import CfgParser


def union(first: Set[str], begins: Set[str]):
    n = len(first)
    first |= begins - {'&'}
    return len(first) != n

# classe para processar uma cfg
class CfgProcessor:
    def __init__(self):
        self.__empty_symbol = '&'
        self.__stack_base_symbol = '$'
        self.cfg: Union[None, Cfg] = None

    # carrega os dados de um arquivo para a classe
    def load_cfg(self, cfg: Cfg):
        self.cfg = cfg
        first = {i: set() for i in self.cfg.non_terminals}
        first.update((i, {i}) for i in self.cfg.terminals)
        first[self.__empty_symbol] = {self.__empty_symbol}

        follow = {i: set() for i in self.cfg.non_terminals}
        follow[self.__empty_symbol] = {self.__stack_base_symbol}
        follow[self.cfg.start_symbol] = {self.__stack_base_symbol}

        epsilon = {self.__empty_symbol}

        while True:
            updated = False

            for prod in self.cfg.productions:
                # calucla o conjunto first
                for symbol in prod.body:
                    updated |= union(first[prod.head], first[symbol])

                    if symbol not in epsilon:
                        break

                else:
                    first[prod.head] |= {self.__empty_symbol}
                    updated |= union(epsilon, {prod.head})

                # calcula o conjunto follow
                aux = follow[prod.head]
                for symbol in reversed(prod.body):
                    if symbol in follow:
                        updated |= union(follow[symbol], aux)

                    if symbol in epsilon:
                        aux = aux.union(first[symbol])
                    else:
                        aux = first[symbol]

            if not updated:
                break

        self.__first = first
        self.__follow = follow
        self.__epsilon = epsilon

    # importa e le um arquivo com uma cfg
    def read(self, filepath: str):
        parser = CfgParser()
        self.load_cfg(parser.parse(filepath))

    # retorna as producoes
    def get_productions_of(self, head: str) -> List[Production]:
        return list(filter(lambda k: k.head == head, self.cfg.productions))

    # retorna as producoes com um simbolo especifico
    def get_productions_with(self, symbol) -> List[Production]:
        return list(filter(lambda k: symbol in k.body, self.cfg.productions))

    # verifica se é terminal
    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.cfg.terminals

    # verifica se é vazio
    def is_empty(self, symbol) -> bool:
        return symbol == self.__empty_symbol

    # verifica se é nao terminal
    def is_non_terminal(self, symbol: str) -> bool:
        return not self.is_terminal(symbol) and not self.is_empty(symbol)

    # retorna os first
    def first(self, symbol: str) -> Set[str]:
        return self.__first[symbol]

    # retorna os follow
    def follow(self, symbol: str) -> Set[str]:
        return self.__follow[symbol]

    def first_of_prod_body(self, body: List[str]) -> Set[str]:
        first = set()
        for symbol in body:
            symbol_first = self.first(symbol)

            first |= self.first(symbol) - {self.__empty_symbol}

            if self.__empty_symbol not in symbol_first:
                break

        else:
            first |= {self.__empty_symbol}

        return first

    # verifica o primeiro teorema
    # first(alpha) interseçao first(beta) = {}
    def __theorem_first_clause(self, prod1: Production, prod2: Production) -> bool:
        prod1_first = self.first_of_prod_body(prod1.body)
        prod2_first = self.first_of_prod_body(prod2.body)
        valid = prod1_first.intersection(prod2_first) == set()

        if not valid:
            print('Prod1 first:: %s ' % prod1_first)
            print('Prod2 first:: %s ' % prod2_first)
            print('First theorem failed')

        return valid

    # verifica o segundo teorema
    # If beta ->* &, First(alpha) intersect Follow(A) = {}
    # If alpha ->* &, First(beta) intersect Follow(A) = {}
    # prod.body ->* & == First(prod.body) contains empty_symbol
    def __theorem_second_clause(self, prod1: Production,prod2: Production) -> bool:
        if prod1.head != prod2.head:
            print('Theorem do not apply to different heads: %s, %s' % (prod1, prod2))
            exit(1)

        valid = True
        head_follow = self.follow(prod1.head)
        prod1_body_first = self.first_of_prod_body(prod1.body)
        prod2_body_first = self.first_of_prod_body(prod2.body)

        if self.__empty_symbol in prod2_body_first:
            valid &= prod1_body_first.intersection(head_follow) == set()

        if self.__empty_symbol in prod1_body_first:
            valid &= prod2_body_first.intersection(head_follow) == set()

        if not valid:
            print('Second theorem failed')
            print('Prod1 first: %s' % prod1_body_first)
            print('Prod2 first: %s' % prod2_body_first)
            print('Head follow: %s' % head_follow)

        return valid

    # aplica os teoremas para todas as producoes de um nao terminal
    def __apply_theorem_all_prods_of(self, nt: str) -> bool:
        prods = self.get_productions_of(nt)
        for p1, p2 in combinations(prods, 2):
            first_clause = self.__theorem_first_clause(p1, p2)
            second_clause = self.__theorem_second_clause(p1, p2)
            if not (first_clause and second_clause):
                print('Grammar is not LL(1) due to: %s, %s' % (p1, p2))
                return False

        return True

    # verfica se é ll1 através dos teoremas
    def is_ll1(self) -> bool:
        for nt in self.cfg.non_terminals:
            if not self.__apply_theorem_all_prods_of(nt):
                return False

        return True

    # se é ll1, gera a matriz
    def generate_matrix(self) -> SyntaticAnalyserMatrix:
        """Generate the analyser matrix, if the grammar is LL(1)"""
        if not self.is_ll1():
            print('Cannot generate matrix for non LL(1) grammar')
            exit()

        mat = SyntaticAnalyserMatrix(
            self.cfg.terminals, self.cfg.non_terminals)

        for prod in self.cfg.productions:
            body_first = self.first_of_prod_body(prod.body)
            for terminal in body_first - {self.__empty_symbol}:
                mat.set_prod(prod.head, terminal, prod)

            if self.__empty_symbol in body_first:
                for terminal in self.follow(prod.head):
                    mat.set_prod(prod.head, terminal, prod)

        return mat
