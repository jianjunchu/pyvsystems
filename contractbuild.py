import itertools
import os
import struct

from pyvsystems import deser
from pyvsystems.dataentry import DataEntry, Type
from pyvsystems.deser import serialize_string



class ContractBuild:
    # texture
    trigger_para = ["max", "unity", "tokenDescription", "signer"]
    supersede_para = ["newIssuer", "maker"]
    issue_para = ["amount", "tokenIndex", "issuer"]
    destroy_para = ["amount", "tokenIndex", "issuer"]
    split_para = ["newUnity", "tokenIndex", "issuer"]
    send_para = ["receipt", "amount", "tokenIndex", "caller"]
    transfer_para = ["sender", "receipt", "amount", "tokenIndex"]
    deposit_para = ["sender", "smart", "amount", "tokenIndex"]
    withdraw_para = ["smart", "receipt", "amount", "tokenIndex"]
    total_supply_para = ["tokenIndex", "total"]
    max_supply_para = ["tokenIndex", "max"]
    balance_of_para = ["address", "tokenIndex", "balance"]
    get_issuer_para = ["issuer"]

    # statevar
    state_var_issuer = bytes([0])
    state_var_maker = bytes([1])

    # datatype
    public_key = bytes([1])
    address = bytes([2])
    amount = bytes([3])
    int32 = bytes([4])
    short_text = bytes([5])
    contract_account = bytes([6])
    account = bytes([7])

    # assertype
    gteq_zero_assert = bytes([1])
    lteq_assert = bytes([2])
    lt_int64_assert = bytes([3])
    gt_zero_assert = bytes([4])
    eq_assert =bytes([5])
    is_caller_origin_assert = bytes([6])
    is_signer_origin_assert = bytes([7])

    # cdbvtype
    set_cdbv = bytes([1])

    # cdbvrtype
    get_cdbvr = bytes([1])

    # loadtype
    signer_load = bytes([1])
    caller_load =bytes([2])

    # opctype
    assert_opc = bytes([1])
    load_opc = bytes([2])
    cdbv_opc = bytes([3])
    cdbvr_opc = bytes([4])
    tdb_opc = bytes([5])
    tdbr_opc = bytes([6])
    tdba_opc = bytes([7])
    tdbar_opc = bytes([8])
    return_opc = bytes([9])

    # tdbatype
    deposit_tdba = bytes([1])
    withdraw_tdba = bytes([2])
    transfer_tdba = bytes([3])

    # tdbartype
    balance_tdbar = bytes([1])

    # tdbtype
    new_token_tdb = bytes([1])
    split_tdb = bytes([2])

    # tdbrtype
    get_tdbr = bytes([1])
    total_tdbr = bytes([2])

    # funid
    trigger = 0
    supersede = 0
    issue = 1
    destroy = 2
    split = 3
    send = 4
    transfer = 5
    deposit = 6
    withdraw = 7
    total_supply = 8
    max_supply = 9
    balance_of = 10
    get_issuer = 11

    supersede_index = bytes([0])
    issue_index = bytes([1])
    destroy_index = bytes([2])
    split_index = bytes([3])
    send_index = bytes([4])
    transfer_index = bytes([5])
    deposit_index = bytes([6])
    withdraw_index = bytes([7])
    total_supply_index = bytes([8])
    max_supply_index = bytes([9])
    balance_of_index = bytes([10])
    get_issuer_index = bytes([11])

    # funtype
    non_return_type = bytes('',encoding ='utf-8')
    on_init_trigger_type = 0
    public_func_type = 0

    # datastack
    trigger_input_max_index = bytes([0])
    trigger_input_unity_index = bytes([1])
    trigger_input_short_text_index = bytes([2])
    trigger_input_issuer_load_index = bytes([3])

    supersede_input_new_issuer_index = bytes([0])
    supersede_input_maker = bytes([1])

    split_input_new_unity_index = bytes([0])
    split_input_token_index = bytes([1])
    split_input_issuer_get_index = bytes([2])

    destroy_input_destroy_amount_index = bytes([0])
    destroy_input_token_index = bytes([1])
    destroy_input_issuer_get_index = bytes([2])

    issue_input_amount_index = bytes([0])
    issue_input_token_index = bytes([1])
    issue_input_issuer_get_index = bytes([2])

    send_input_recipient_index = bytes([0])
    send_input_amount_index = bytes([1])
    send_input_token_index = bytes([2])
    send_input_sender_index = bytes([3])

    transfer_input_sender_index = bytes([0])
    transfer_input_recipient_index = bytes([1])
    transfer_input_amount_index = bytes([2])
    transfer_input_token_index = bytes([3])

    deposit_input_sender_index = bytes([0])
    deposit_input_smart_contract_index = bytes([1])
    deposit_input_amount_index = bytes([2])
    deposit_input_token_index = bytes([3])

    withdraw_input_smart_contract_index = bytes([0])
    withdraw_input_recipient_index = bytes([1])
    withdraw_input_amount_index = bytes([2])
    withdraw_input_token_index = bytes([3])

    total_supply_input_token_index = bytes([0])

    max_supply_input_token_index = bytes([0])

    balance_of_input_account_index = bytes([0])
    balance_of_input_token_index = bytes([1])

    def contract_builder(self, language_code, language_version, split=False):
        lang_code = self.language_code_builder(language_code)
        lang_ver = self.language_version_builder(language_version)
        trigger = self.trigger_builder()
        descriptor = self.descriptor_builder(split)
        state_var = self.state_var_builder()
        texture = self.texture_builder(split)
        return lang_code + lang_ver + trigger + descriptor + state_var + texture

    # OpcId
    def assert_gteq_zero_gen(self):
        return self.opc_assert_gteq_zero()
    def assert_lteq_gen(self):
        return self.opc_assert_lteq()
    def assert_lt_int64_gen(self):
        return self.opc_assert_lt_int64()
    def assert_gt_zero_gen(self):
        return self.opc_assert_gt_zero()
    def assert_eq_gen(self):
        return self.opc_assert_eq()
    def assert_is_caller_origin_gen(self):
        return self.opc_assert_is_caller_origin()
    def assert_is_signer_origin_gen(self):
        return self.opc_assert_is_signer_origin()
    def load_signer_gen(self):
        return self.opc_load_signer()
    def load_caller_gen(self):
        return self.opc_load_caller()
    def cdbv_set_gen(self):
        return self.opc_cdbv_set()
    def cdbvr_get_gen(self):
        return self.opc_cdbvr_get()
    def tdb_new_token_gen(self):
        return self.opc_tdb_new_token()
    def tdb_split_gen(self):
        return self.opc_tdb_split()
    def tdbr_opc_max(self):
        return self.opc_tdbr_opc_max()
    def tdbr_opc_total_gen(self):
        return self.opc_tdbr_opc_total()
    def tdba_deposit_gen(self):
        return self.opc_tdba_deposit()
    def tdba_withdraw_gen(self):
        return self.opc_tdba_withdraw()
    def tdba_transfer_gen(self):
        return self.opc_tdba_transfer()
    def tdbar_balance_gen(self):
        return self.opc_tdbar_balance()

    def opc_assert_gteq_zero(self):
        return self.assert_opc + self.gteq_zero_assert

    def opc_assert_lteq(self):
        return self.assert_opc + self.lteq_assert

    def opc_assert_lt_int64(self):
        return self.assert_opc + self.lt_int64_assert

    def opc_assert_gt_zero(self):
        return self.assert_opc + self.gt_zero_assert

    def opc_assert_eq(self):
        return self.assert_opc + self.eq_assert

    def opc_assert_is_caller_origin(self):
        return self.assert_opc + self.is_caller_origin_assert

    def opc_assert_is_signer_origin(self):
        return self.assert_opc + self.is_signer_origin_assert

    def opc_load_signer(self):
        return self.load_opc + self.signer_load

    def opc_load_caller(self):
        return self.load_opc + self.caller_load

    def opc_cdbv_set(self):
        return self.cdbv_opc + self.set_cdbv

    def opc_cdbvr_get(self):
        return self.cdbvr_opc + self.get_cdbvr

    def opc_tdb_new_token(self):
        return self.tdb_opc + self.new_token_tdb

    def opc_tdb_split(self):
        return self.tdb_opc + self.split_tdb

    def opc_tdbr_opc_max(self):
        return self.tdbr_opc + self.get_tdbr

    def opc_tdbr_opc_total(self):
        return self.tdbr_opc + self.total_tdbr

    def opc_tdba_deposit(self):
        return self.tdba_opc + self.deposit_tdba

    def opc_tdba_withdraw(self):
        return self.tdba_opc + self.withdraw_tdba

    def opc_tdba_transfer(self):
        return self.tdba_opc + self.transfer_tdba

    def opc_tdbar_balance(self):
        return self.tdbar_opc + self.balance_tdbar

    def opc_return_value(self):
        return self.return_opc + bytes([1])

    # languageCode
    def language_code_builder(self, code):
        language_code = deser.serialize_string(code)
        return language_code

    # languageVersion
    def language_version_builder(self, version):
        return struct.pack(">I", version)

    # trigger
    def trigger_builder(self):
        return deser.serialize_array(self.trigger_fun_gen())

    # descriptor
    def descriptor_builder(self, split):
        if(split is False):
            descriptor = deser.serialize_arrays(
                [self.supersede_fun_gen(), self.issue_fun_gen(), self.destroy_fun_gen(),
                 self.send_fun_gen(), self.transfer_fun_gen(), self.deposit_fun_gen(), self.withdraw_fun_gen(), self.total_supply_fun_gen(),
                 self.max_supply_fun_gen(), self.balance_of_fun_gen(), self.get_issuer_fun_gen()])
        else:
            descriptor = deser.serialize_arrays([self.supersede_fun_gen(), self.issue_fun_gen(), self.destroy_fun_gen(), self.split_fun_gen(), self.send_fun_gen(),
                                                self.transfer_fun_gen(), self.deposit_fun_gen(), self.withdraw_fun_gen(), self.total_supply_fun_gen(),
                                                self.max_supply_fun_gen(), self.balance_of_fun_gen(), self.get_issuer_fun_gen()])

        return deser.serialize_array(descriptor)


    # stateVar
    def state_var_builder(self):
        state_var = self.state_var_gen([self.state_var_issuer + self.address, self.state_var_maker + self.address])
        return deser.serialize_array(state_var)

    # texture
    def texture_builder(self, split):
        self._fixed_size = 4
        self.state_var_name = ["issuer", "maker"]
        self.state_var_texture = deser.serialize_arrays([deser.serialize_string(name) for name in self.state_var_name])
        self.trigger_texture = deser.serialize_arrays([self.trigger_func_bytes()])
        if(split is False):
            self.descriptor_texture = deser.serialize_arrays([self.supersede_func_bytes(),
                                                            self.issue_func_bytes(),
                                                            self.destroy_func_bytes(),
                                                            self.send_func_bytes(),
                                                            self.transfer_func_bytes(),
                                                            self.deposit_func_bytes(),
                                                            self.withdraw_func_bytes(),
                                                            self.total_supply_func_bytes(),
                                                            self.max_supply_func_bytes(),
                                                            self.balance_of_func_bytes(),
                                                            self.get_issuer_func_bytes()])
        else:
            self.descriptor_texture = deser.serialize_arrays([self.supersede_func_bytes(),
                                                            self.issue_func_bytes(),
                                                            self.destroy_func_bytes(),
                                                            self.split_func_bytes(),
                                                            self.send_func_bytes(),
                                                            self.transfer_func_bytes(),
                                                            self.deposit_func_bytes(),
                                                            self.withdraw_func_bytes(),
                                                            self.total_supply_func_bytes(),
                                                            self.max_supply_func_bytes(),
                                                            self.balance_of_func_bytes(),
                                                            self.get_issuer_func_bytes()])

        self.texture_right_gen = self.texture_gen(self.trigger_texture, self.descriptor_texture, self.state_var_texture)
        return self.texture_right_gen

    def texture_random_gen(self):
        texture = bytearray(os.urandom(self._fixed_size))
        return texture

    def texture_gen(self, trigger, description, state_var):
        return deser.serialize_arrays([trigger, description, state_var])

    def texture_fun_gen(self, name, ret, para):
        func_byte = deser.serialize_array(deser.serialize_string(name))
        ret_byte = deser.serialize_array(deser.serialize_arrays([deser.serialize_string(r) for r in ret]))
        para_byte = deser.serialize_arrays([deser.serialize_string(p) for p in para])
        texture = func_byte + ret_byte + para_byte
        return texture


    def trigger_func_bytes(self):
        return self.texture_fun_gen("trigger", [], self.trigger_para)

    def supersede_func_bytes(self):
        return self.texture_fun_gen("supersede", [], self.supersede_para)

    def issue_func_bytes(self):
        return self.texture_fun_gen("issue", [], self.issue_para)

    def destroy_func_bytes(self):
        return self.texture_fun_gen("destroy", [], self.destroy_para)

    def split_func_bytes(self):
        return self.texture_fun_gen("split", [], self.split_para)

    def send_func_bytes(self):
        return self.texture_fun_gen("send", [], self.send_para)

    def transfer_func_bytes(self):
        return self.texture_fun_gen("transfer", [], self.transfer_para)

    def deposit_func_bytes(self):
        return self.texture_fun_gen("deposit", [], self.deposit_para)

    def withdraw_func_bytes(self):
        return self.texture_fun_gen("withdraw", [], self.withdraw_para)

    def total_supply_func_bytes(self):
        return self.texture_fun_gen("totalSupply", ["total"], self.total_supply_para)

    def max_supply_func_bytes(self):
        return self.texture_fun_gen("maxSupply", ["max"], self.max_supply_para)

    def balance_of_func_bytes(self):
        return self.texture_fun_gen("balanceOf", ["balance"], self.balance_of_para)

    def get_issuer_func_bytes(self):
        return self.texture_fun_gen("getIssuer", ["issuer"], self.get_issuer_para)


    # statevar
    def state_var_random_gen(self):
        self.fixed_size = 2
        state_var = bytearray(os.urandom(self.fixed_size))
        return state_var

    def state_var_gen(self, state_vars):
        state_vars = deser.serialize_arrays(state_vars)
        return state_vars

    def a_function_gen(self, fun_idx, fun_type, proto_type, list_opc):
        fun = fun_idx + fun_type + proto_type + list_opc
        return fun

    def trigger_fun_gen(self):
        fun = self.a_function_gen(self.trigger_fun_id_gen(), self.trigger_fun_type_gen(), self.proto_type_trigger_gen(), self.trigger_opc_line_gen())
        return fun

    def supersede_fun_gen(self):
        fun = self.a_function_gen(self.supersede_fun_id_gen(), self.supersede_fun_type_gen(), self.proto_type_supersede_gen(), self.supersede_opc_line_gen())
        return fun

    def issue_fun_gen(self):
        fun = self.a_function_gen(self.issue_fun_id_gen(), self.issue_fun_type_gen(), self.proto_type_issue_gen(), self.issue_opc_line_gen())
        return fun

    def destroy_fun_gen(self):
        fun = self.a_function_gen(self.destroy_fun_id_gen(), self.destroy_fun_type_gen(), self.proto_type_destroy_gen(), self.destroy_opc_line_gen())
        return fun

    def split_fun_gen(self):
        fun = self.a_function_gen(self.split_fun_id_gen(), self.split_fun_type_gen(), self.proto_type_split_gen(), self.split_opc_line_gen())
        return fun

    def send_fun_gen(self):
        fun = self.a_function_gen(self.send_fun_id_gen(), self.send_fun_type_gen(), self.proto_type_send_gen(), self.send_opc_line_gen())
        return fun

    def transfer_fun_gen(self):
        fun = self.a_function_gen(self.transfer_fun_id_gen(), self.transfer_fun_type_gen(), self.proto_type_transfer_gen(), self.transfer_opc_line_gen())
        return fun

    def deposit_fun_gen(self):
        fun = self.a_function_gen(self.deposit_fun_id_gen(), self.deposit_fun_type_gen(), self.proto_type_deposit_gen(), self.deposit_opc_line_gen())
        return fun

    def withdraw_fun_gen(self):
        fun = self.a_function_gen(self.withdraw_fun_id_gen(), self.withdraw_fun_type_gen(), self.proto_type_withdraw_gen(), self.withdraw_opc_line_gen())
        return fun

    def total_supply_fun_gen(self):
        fun = self.a_function_gen(self.total_supply_fun_id_gen(), self.total_supply_fun_type_gen(), self.proto_type_total_supply_gen(), self.total_supply_opc_line_gen())
        return fun

    def max_supply_fun_gen(self):
        fun = self.a_function_gen(self.max_supply_fun_id_gen(), self.max_supply_fun_type_gen(), self.proto_type_max_supply_gen(), self.max_supply_opc_line_gen())
        return fun

    def balance_of_fun_gen(self):
        fun = self.a_function_gen(self.balance_of_fun_id_gen(), self.balance_of_fun_type_gen(), self.proto_type_balance_of_gen(), self.balance_of_opc_line_gen())
        return fun

    def get_issuer_fun_gen(self):
        fun = self.a_function_gen(self.get_issuer_fun_id_gen(), self.get_issuer_fun_type_gen(), self.proto_type_get_issuer_gen(), self.get_issuer_opc_line_gen())
        return fun

    # funid
    def trigger_fun_id_gen(self):
        return struct.pack(">H", self.trigger)
    def supersede_fun_id_gen(self):
        return struct.pack(">H", self.supersede)
    def issue_fun_id_gen(self):
        return struct.pack(">H", self.issue)
    def destroy_fun_id_gen(self):
        return struct.pack(">H", self.destroy)
    def split_fun_id_gen(self):
        return struct.pack(">H", self.split)
    def send_fun_id_gen(self):
        return struct.pack(">H", self.send)
    def transfer_fun_id_gen(self):
        return struct.pack(">H", self.transfer)
    def deposit_fun_id_gen(self):
        return struct.pack(">H", self.deposit)
    def withdraw_fun_id_gen(self):
        return struct.pack(">H", self.withdraw)
    def total_supply_fun_id_gen(self):
        return struct.pack(">H", self.total_supply)
    def max_supply_fun_id_gen(self):
        return struct.pack(">H", self.max_supply)
    def balance_of_fun_id_gen(self):
        return struct.pack(">H", self.balance_of)
    def get_issuer_fun_id_gen(self):
        return struct.pack(">H", self.get_issuer)

    # funtype
    def trigger_fun_type_gen(self):
        return bytes([self.on_init_trigger_type])
    def supersede_fun_type_gen(self):
        return bytes([self.public_func_type])
    def issue_fun_type_gen(self):
        return bytes([self.public_func_type])
    def destroy_fun_type_gen(self):
        return bytes([self.public_func_type])
    def split_fun_type_gen(self):
        return bytes([self.public_func_type])
    def send_fun_type_gen(self):
        return bytes([self.public_func_type])
    def transfer_fun_type_gen(self):
        return bytes([self.public_func_type])
    def deposit_fun_type_gen(self):
        return bytes([self.public_func_type])
    def withdraw_fun_type_gen(self):
        return bytes([self.public_func_type])
    def total_supply_fun_type_gen(self):
        return bytes([self.public_func_type])
    def max_supply_fun_type_gen(self):
        return bytes([self.public_func_type])
    def balance_of_fun_type_gen(self):
        return bytes([self.public_func_type])
    def get_issuer_fun_type_gen(self):
        return bytes([self.public_func_type])

    # prototype
    def proto_type_gen(self, return_type, list_para_types):
        proto_type = deser.serialize_array(return_type) + deser.serialize_array(list_para_types)
        return proto_type

    def trigger_para_type_wrong(self):
        return [self.amount, self.amount]

    def trigger_para_type(self):
        return [self.amount, self.amount, self.short_text]

    def supersede_para_type(self):
        return [self.account]

    def issue_para_type(self):
        return [self.amount, self.int32]

    def destroy_para_type(self):
        return [self.amount + self.int32]

    def split_para_type(self):
        return [self.amount + self.int32]

    def send_para_type(self):
        return [self.account + self.amount + self.int32]

    def transfer_para_type(self):
        return [self.account + self.account + self.amount + self.int32]

    def deposit_para_type(self):
        return [self.account + self.contract_account + self.amount + self.int32]

    def withdraw_para_type(self):
        return [self.contract_account + self.account + self.amount + self.int32]

    def total_supply_para_type(self):
        return [self.int32]

    def max_supply_para_type(self):
        return [self.int32]

    def balance_of_para_type(self):
        return [self.account + self.int32]

    def get_issuer_para_type(self):
        return [bytes('',encoding ='utf-8')]

    def proto_type_trigger_wrong_gen(self):
        return self.proto_type_gen(self.non_return_type, self.trigger_para_type_wrong())

    def proto_type_trigger_gen(self):
        return self.proto_type_gen(self.non_return_type, self.trigger_para_type())

    def proto_type_supersede_gen(self):
        return self.proto_type_gen(self.non_return_type, self.supersede_para_type())

    def proto_type_issue_gen(self):
        return self.proto_type_gen(self.non_return_type, self.issue_para_type())

    def proto_type_destroy_gen(self):
        return self.proto_type_gen(self.non_return_type, self.destroy_para_type())

    def proto_type_split_gen(self):
        return self.proto_type_gen(self.non_return_type, self.split_para_type())

    def proto_type_send_gen(self):
        return self.proto_type_gen(self.non_return_type, self.send_para_type())

    def proto_type_transfer_gen(self):
        return self.proto_type_gen(self.non_return_type, self.transfer_para_type())

    def proto_type_deposit_gen(self):
        return self.proto_type_gen(self.non_return_type, self.deposit_para_type())

    def proto_type_withdraw_gen(self):
        return self.proto_type_gen(self.non_return_type, self.withdraw_para_type())

    def proto_type_total_supply_gen(self):
        return self.proto_type_gen([self.amount], self.total_supply_para_type())

    def proto_type_max_supply_gen(self):
        return self.proto_type_gen([self.amount], self.max_supply_para_type())

    def proto_type_balance_of_gen(self):
        return self.proto_type_gen([self.amount], self.balance_of_para_type())

    def proto_type_get_issuer_gen(self):
        return self.proto_type_gen([self.account], self.get_issuer_para_type())


    # listopc
    def list_opc_gen(self, ids, index_input):
        length = struct.pack(">H", sum(list(map(lambda x: len(x[0]+x[1])+2, list(zip(ids, index_input))))) + 2)
        num_opc = struct.pack(">H", len(ids))
        list_opc = bytes(itertools.chain.from_iterable(list(map(lambda x: struct.pack(">H",len(x[0]+x[1]))+x[0]+x[1], list(zip(ids, index_input))))))
        len_list_opc = length + num_opc + list_opc
        return len_list_opc


    def trigger_opc_line_wrong_tdb_gen(self):
        return self.list_opc_gen(self.trigger_wrong_tdb_opc(), self.trigger_opc_index())

    def trigger_opc_line_gen(self):
        return self.list_opc_gen(self.trigger_opc(), self.trigger_opc_index())

    def supersede_opc_line_gen(self):
        return self.list_opc_gen(self.supersede_opc(), self.supersede_opc_index())

    def issue_opc_line_gen(self):
        return self.list_opc_gen(self.issue_opc(), self.issue_opc_index())

    def destroy_opc_line_gen(self):
        return self.list_opc_gen(self.destroy_opc(), self.destroy_opc_index())

    def split_opc_line_gen(self):
        return self.list_opc_gen(self.split_opc(), self.split_opc_index())

    def send_opc_line_gen(self):
        return self.list_opc_gen(self.send_opc(), self.send_opc_index())

    def transfer_opc_line_gen(self):
        return self.list_opc_gen(self.transfer_opc(), self.transfer_opc_index())

    def deposit_opc_line_gen(self):
        return self.list_opc_gen(self.deposit_opc(), self.deposit_opc_index())

    def withdraw_opc_line_gen(self):
        return self.list_opc_gen(self.withdraw_opc(), self.withdraw_opc_index())

    def total_supply_opc_line_gen(self):
        return self.list_opc_gen(self.total_supply_opc(), self.total_supply_opc_index())

    def max_supply_opc_line_gen(self):
        return self.list_opc_gen(self.max_supply_opc(), self.max_supply_opc_index())

    def balance_of_opc_line_gen(self):
        return self.list_opc_gen(self.balance_of_opc(), self.balance_of_opc_index())

    def get_issuer_opc_line_gen(self):
        return self.list_opc_gen(self.get_issuer_opc(), self.get_issuer_opc_index())

    def opc_load_signer_index(self):
        return bytes([3])

    def opc_load_caller_index(self):
        return bytes([3])

    def trigger_opc_cdbv_set_signer_index(self):
        return self.state_var_issuer + self.trigger_input_issuer_load_index

    def trigger_opc_cdbv_set_maker_index(self):
        return self.state_var_maker + self.trigger_input_issuer_load_index

    def trigger_opc_tdb_new_token_index(self):
        return self.trigger_input_max_index + self.trigger_input_unity_index + self.trigger_input_short_text_index

    def trigger_wrong_tdb_opc(self):
        return [self.opc_load_signer(), self.opc_cdbv_set(), self.opc_cdbv_set(), bytes([5]), bytes([3])]

    def trigger_opc(self):
        return [self.opc_load_signer(), self.opc_cdbv_set(), self.opc_cdbv_set(), self.opc_tdb_new_token()]

    def trigger_opc_index(self):
        return [self.opc_load_signer_index(), self.trigger_opc_cdbv_set_signer_index(), self.trigger_opc_cdbv_set_maker_index(), self.trigger_opc_tdb_new_token_index()]

    def supersede_opc_cdbvr_get_index(self):
        return self.state_var_maker + bytes([1])

    def supersede_assert_is_signer_origin_index(self):
        return self.supersede_input_maker

    def supersede_opc_cdbv_set_index(self):
        return self.state_var_issuer + self.supersede_input_new_issuer_index

    def supersede_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_signer_origin(), self.opc_cdbv_set()]

    def supersede_opc_index(self):
        return [self.supersede_opc_cdbvr_get_index(), self.supersede_assert_is_signer_origin_index(), self.supersede_opc_cdbv_set_index()]

    def issue_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([2])

    def issue_opc_assert_is_caller_origin_index(self):
        return self.issue_input_issuer_get_index

    def issue_opc_tdba_deposit_index(self):
        return self.issue_input_issuer_get_index + self.issue_input_amount_index + self.issue_input_token_index

    def issue_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdba_deposit()]

    def issue_opc_index(self):
        return [self.issue_opc_cdbvr_get_index(), self.issue_opc_assert_is_caller_origin_index(), self.issue_opc_tdba_deposit_index()]

    def destroy_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([2])

    def destroy_opc_assert_is_caller_origin_index(self):
        return self.destroy_input_issuer_get_index

    def destroy_opc_tdba_withdraw_index(self):
        return self.destroy_input_issuer_get_index + self.destroy_input_destroy_amount_index + self.destroy_input_token_index

    def destroy_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdba_withdraw()]

    def destroy_opc_index(self):
        return [self.destroy_opc_cdbvr_get_index(), self.destroy_opc_assert_is_caller_origin_index(), self.destroy_opc_tdba_withdraw_index()]

    def split_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([2])

    def split_opc_assert_is_caller_origin_index(self):
        return self.split_input_issuer_get_index

    def split_opc_tdb_split_index(self):
        return self.split_input_new_unity_index + self.split_input_token_index

    def split_opc(self):
        return [self.opc_cdbvr_get(), self.opc_assert_is_caller_origin(), self.opc_tdb_split()]

    def split_opc_index(self):
        return [self.split_opc_cdbvr_get_index(), self.split_opc_assert_is_caller_origin_index(), self.split_opc_tdb_split_index()]

    def send_opc_tdba_transfer_index(self):
        return self.send_input_sender_index + self.send_input_recipient_index + self.send_input_amount_index + self.send_input_token_index

    def send_opc(self):
        return [self.opc_load_caller(), self.opc_tdba_transfer()]

    def send_opc_index(self):
        return [self.opc_load_caller_index(), self.send_opc_tdba_transfer_index()]

    def transfer_opc_assert_is_caller_origin_index(self):
        return self.transfer_input_sender_index

    def transfer_opc_tdba_transfer_index(self):
        return self.transfer_input_sender_index + self.transfer_input_recipient_index + self.transfer_input_amount_index + self.transfer_input_token_index

    def transfer_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def transfer_opc_index(self):
        return [self.transfer_opc_assert_is_caller_origin_index(), self.transfer_opc_tdba_transfer_index()]

    def deposit_opc_assert_is_caller_origin_index(self):
        return self.deposit_input_sender_index

    def deposit_opc_tdba_transfer_index(self):
        return self.deposit_input_sender_index + self.deposit_input_smart_contract_index + self.deposit_input_amount_index + self.deposit_input_token_index

    def deposit_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def deposit_opc_index(self):
        return [self.deposit_opc_assert_is_caller_origin_index(), self.deposit_opc_tdba_transfer_index()]

    def withdraw_opc_assert_is_caller_origin_index(self):
        return self.withdraw_input_recipient_index

    def withdraw_opc_tdba_transfer_index(self):
        return self.withdraw_input_smart_contract_index + self.withdraw_input_recipient_index + self.withdraw_input_amount_index + self.withdraw_input_token_index

    def withdraw_opc(self):
        return [self.opc_assert_is_caller_origin(), self.opc_tdba_transfer()]

    def withdraw_opc_index(self):
        return [self.withdraw_opc_assert_is_caller_origin_index(), self.withdraw_opc_tdba_transfer_index()]

    def total_supply_opc_tdbr_total_index(self):
        return self.total_supply_input_token_index + bytes([1])

    def total_supply_opc(self):
        return [self.opc_tdbr_opc_total(), self.opc_return_value()]

    def total_supply_opc_index(self):
        return [self.total_supply_opc_tdbr_total_index(), bytes([1])]

    def max_supply_opc_tdbr_max_index(self):
        return self.max_supply_input_token_index + bytes([1])

    def max_supply_opc(self):
        return [self.opc_tdbr_opc_max(), self.opc_return_value()]

    def max_supply_opc_index(self):
        return [self.max_supply_opc_tdbr_max_index(), bytes([1])]

    def balance_of_opc_tdbar_balance_index(self):
        return self.balance_of_input_account_index + self.balance_of_input_token_index  + bytes([2])

    def balance_of_opc(self):
        return [self.opc_tdbar_balance(), self.opc_return_value()]

    def balance_of_opc_index(self):
        return [self.balance_of_opc_tdbar_balance_index(), bytes([2])]

    def get_issuer_opc_cdbvr_get_index(self):
        return self.state_var_issuer + bytes([0])

    def get_issuer_opc(self):
        return [self.opc_cdbvr_get(), self.opc_return_value()]

    def get_issuer_opc_index(self):
        return [self.get_issuer_opc_cdbvr_get_index(), bytes([0])]

    # datastack
    @staticmethod
    def init_data_stack_gen(max, unity, desc):
        max = DataEntry(max, Type.amount)
        unit = DataEntry(unity, Type.amount)
        short_txt = DataEntry(desc, Type.short_text)
        init_data_stack = [max.bytes, unit.bytes, short_txt.bytes]
        return deser.serialize_array(init_data_stack)

    @staticmethod
    def supersede_data_stack_gen(new_iss):
        iss = DataEntry(new_iss, Type.address)
        supersede_data_stack = [iss.bytes]
        return deser.serialize_array(supersede_data_stack)

    @staticmethod
    def split_data_stack_gen(new_unity, token_id):
        unit = DataEntry(new_unity, Type.amount)
        index = DataEntry(token_id, Type.int32)
        split_data_stack = [unit.bytes, index.bytes]
        return deser.serialize_array(split_data_stack)

    @staticmethod
    def destroy_data_stack_gen(amount, token_id):
        am = DataEntry(amount, Type.amount)
        index = DataEntry(token_id, Type.int32)
        destroy_data_stack = [am.bytes, index.bytes]
        return deser.serialize_array(destroy_data_stack)

    @staticmethod
    def issue_data_stack_gen(amount, token_id):
        max = DataEntry(amount, Type.amount)
        index = DataEntry(token_id, Type.int32)
        issue_data_stack = [max.bytes, index.bytes]
        return deser.serialize_array(issue_data_stack)

    @staticmethod
    def send_data_stack_gen(recipient, amount, token_id):
        reci = DataEntry(recipient, Type.address)
        am = DataEntry(amount, Type.amount)
        index = DataEntry(token_id, Type.int32)
        send_data_stack = [reci.bytes, am.bytes, index.bytes]
        return deser.serialize_array(send_data_stack)

    @staticmethod
    def transfer_data_stack_gen(sender, recipient, amount, token_id):
        se = DataEntry(sender, Type.address)
        reci = DataEntry(recipient, Type.address)
        am = DataEntry(amount, Type.amount)
        index = DataEntry(token_id, Type.int32)
        transfer_data_stack = [se.bytes, reci.bytes, am.bytes, index.bytes]
        return deser.serialize_array(transfer_data_stack)

    @staticmethod
    def deposit_data_stack_gen(sender, smart_contract, amount, token_id):
        se = DataEntry(sender, Type.address)
        sc = DataEntry(smart_contract, Type.address)
        am = DataEntry(amount, Type.amount)
        index = DataEntry(token_id, Type.int32)
        deposit_data_stack = [se.bytes, sc.bytes, am.bytes, index.bytes]
        return deser.serialize_array(deposit_data_stack)

    @staticmethod
    def withdraw_data_stack_gen(smart_contract, recipient, amount, token_id):
        sc = DataEntry(smart_contract.bytes.arr, Type.address)
        reci = DataEntry(recipient.bytes.arr, Type.address)
        am = DataEntry(amount, Type.amount)
        index = DataEntry(token_id, Type.int32)
        withdraw_data_stack = [sc.bytes, reci.bytes, am.bytes, index.bytes]
        return deser.serialize_array(withdraw_data_stack)

    @staticmethod
    def total_supply_data_stack_gen(token_id):
        index = DataEntry(token_id, Type.int32)
        total_supply_data_stack = [index.bytes]
        return deser.serialize_array(total_supply_data_stack)

    @staticmethod
    def max_supply_data_stack_gen(token_id):
        index = DataEntry(token_id, Type.int32)
        max_supply_data_stack = [index.bytes]
        return deser.serialize_array(max_supply_data_stack)

    @staticmethod
    def balance_of_data_stack_gen(account, token_id):
        acc =  DataEntry(account.bytes.arr, Type.address)
        index = DataEntry(token_id, Type.int32)
        balance_of_data_stack = [acc.bytes, index.bytes]
        return deser.serialize_array(balance_of_data_stack)
