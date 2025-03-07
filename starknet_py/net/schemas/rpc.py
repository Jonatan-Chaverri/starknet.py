from marshmallow import EXCLUDE, Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from starknet_py.abi.schemas import ContractAbiEntrySchema
from starknet_py.net.client_models import (
    BlockHashAndNumber,
    BlockStateUpdate,
    BlockTransactionTrace,
    ContractClass,
    ContractsNonce,
    DAMode,
    DeclaredContractHash,
    DeclareTransaction,
    DeclareTransactionResponse,
    DeclareTransactionTrace,
    DeclareTransactionV3,
    DeployAccountTransaction,
    DeployAccountTransactionResponse,
    DeployAccountTransactionTrace,
    DeployAccountTransactionV3,
    DeployedContract,
    DeployTransaction,
    EntryPoint,
    EntryPointsByType,
    EstimatedFee,
    Event,
    EventsChunk,
    ExecutionResources,
    FeePayment,
    FunctionInvocation,
    InvokeTransaction,
    InvokeTransactionTrace,
    InvokeTransactionV3,
    L1HandlerTransaction,
    L1HandlerTransactionTrace,
    L2toL1Message,
    OrderedEvent,
    OrderedMessage,
    PendingBlockStateUpdate,
    PendingStarknetBlock,
    PendingStarknetBlockWithTxHashes,
    ReplacedClass,
    ResourceBounds,
    ResourceBoundsMapping,
    ResourcePrice,
    RevertedFunctionInvocation,
    SentTransactionResponse,
    SierraContractClass,
    SierraEntryPoint,
    SierraEntryPointsByType,
    SimulatedTransaction,
    StarknetBlock,
    StarknetBlockWithTxHashes,
    StateDiff,
    StorageDiffItem,
    SyncStatus,
    TransactionReceipt,
    TransactionStatusResponse,
)
from starknet_py.net.schemas.common import (
    BlockStatusField,
    CallTypeField,
    DAModeField,
    EntryPointTypeField,
    ExecutionStatusField,
    Felt,
    FinalityStatusField,
    NonPrefixedHex,
    NumberAsHex,
    PriceUnitField,
    StatusField,
    StorageEntrySchema,
    TransactionTypeField,
    Uint64,
    Uint128,
)
from starknet_py.net.schemas.utils import (
    _extract_tx_version,
    _replace_invoke_contract_address_with_sender_address,
)

# pylint: disable=unused-argument, no-self-use


class EventSchema(Schema):
    from_address = Felt(data_key="from_address", required=True)
    keys = fields.List(Felt(), data_key="keys", required=True)
    data = fields.List(Felt(), data_key="data", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> Event:
        return Event(**data)


class EventsChunkSchema(Schema):
    events = fields.List(
        fields.Nested(EventSchema(unknown=EXCLUDE)),
        data_key="events",
        required=True,
    )
    continuation_token = fields.String(data_key="continuation_token", load_default=None)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return EventsChunk(**data)


class L2toL1MessageSchema(Schema):
    l2_address = Felt(data_key="from_address", required=True)
    l1_address = Felt(data_key="to_address", required=True)
    payload = fields.List(Felt(), data_key="payload", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> L2toL1Message:
        return L2toL1Message(**data)


class ExecutionResourcesSchema(Schema):
    steps = Felt(data_key="steps", required=True)
    range_check_builtin_applications = Felt(
        data_key="range_check_builtin_applications", load_default=None
    )
    pedersen_builtin_applications = Felt(
        data_key="pedersen_builtin_applications", load_default=None
    )
    poseidon_builtin_applications = Felt(
        data_key="poseidon_builtin_applications", load_default=None
    )
    ec_op_builtin_applications = Felt(
        data_key="ec_op_builtin_applications", load_default=None
    )
    ecdsa_builtin_applications = Felt(
        data_key="ecdsa_builtin_applications", load_default=None
    )
    bitwise_builtin_applications = Felt(
        data_key="bitwise_builtin_applications", load_default=None
    )
    keccak_builtin_applications = Felt(
        data_key="keccak_builtin_applications", load_default=None
    )
    memory_holes = Felt(data_key="memory_holes", load_default=None)

    @post_load
    def make_dataclass(self, data, **kwargs) -> ExecutionResources:
        return ExecutionResources(**data)


class FeePaymentSchema(Schema):
    amount = Felt(data_key="amount", required=True)
    unit = PriceUnitField(data_key="unit", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> FeePayment:
        return FeePayment(**data)


class TransactionReceiptSchema(Schema):
    transaction_hash = Felt(data_key="transaction_hash", required=True)
    execution_status = ExecutionStatusField(data_key="execution_status", required=True)
    finality_status = FinalityStatusField(data_key="finality_status", required=True)
    block_number = fields.Integer(data_key="block_number", load_default=None)
    block_hash = Felt(data_key="block_hash", load_default=None)
    actual_fee = fields.Nested(FeePaymentSchema(), data_key="actual_fee", required=True)
    type = TransactionTypeField(data_key="type", required=True)
    contract_address = Felt(data_key="contract_address", load_default=None)
    revert_reason = fields.String(data_key="revert_reason", load_default=None)
    events = fields.List(
        fields.Nested(EventSchema()), data_key="events", load_default=[]
    )
    messages_sent = fields.List(
        fields.Nested(L2toL1MessageSchema()), data_key="messages_sent", load_default=[]
    )
    message_hash = NumberAsHex(data_key="message_hash", load_default=None)
    execution_resources = fields.Nested(
        ExecutionResourcesSchema(), data_key="execution_resources", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> TransactionReceipt:
        return TransactionReceipt(**data)


class EstimatedFeeSchema(Schema):
    overall_fee = Felt(data_key="overall_fee", required=True)
    gas_price = Felt(data_key="gas_price", required=True)
    gas_consumed = Felt(data_key="gas_consumed", required=True)
    unit = PriceUnitField(data_key="unit", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return EstimatedFee(**data)


class TransactionStatusResponseSchema(Schema):
    finality_status = StatusField(data_key="finality_status", required=True)
    execution_status = ExecutionStatusField(
        data_key="execution_status", load_default=None
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> TransactionStatusResponse:
        return TransactionStatusResponse(**data)


class ResourcePriceSchema(Schema):
    price_in_fri = Felt(data_key="price_in_fri", required=True)
    price_in_wei = Felt(data_key="price_in_wei", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> ResourcePrice:
        return ResourcePrice(**data)


class ResourceBoundsSchema(Schema):
    max_amount = Uint64(data_key="max_amount", required=True)
    max_price_per_unit = Uint128(data_key="max_price_per_unit", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> ResourceBounds:
        return ResourceBounds(**data)


class ResourceBoundsMappingSchema(Schema):
    l1_gas = fields.Nested(ResourceBoundsSchema(), data_key="l1_gas", required=True)
    l2_gas = fields.Nested(ResourceBoundsSchema(), data_key="l2_gas", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> ResourceBoundsMapping:
        return ResourceBoundsMapping(**data)


class TransactionSchema(Schema):
    hash = Felt(data_key="transaction_hash", load_default=None)
    signature = fields.List(Felt(), data_key="signature", load_default=[])
    version = Felt(data_key="version", required=True)


class DeprecatedTransactionSchema(TransactionSchema):
    max_fee = Felt(data_key="max_fee", required=True)


class TransactionV3Schema(TransactionSchema):
    tip = Uint64(data_key="tip", load_default=0)
    nonce_data_availability_mode = DAModeField(
        data_key="nonce_data_availability_mode", load_default=DAMode.L1
    )
    fee_data_availability_mode = DAModeField(
        data_key="fee_data_availability_mode", load_default=DAMode.L1
    )
    paymaster_data = fields.List(Felt(), data_key="paymaster_data", load_default=[])
    resource_bounds = fields.Nested(
        ResourceBoundsMappingSchema(), data_key="resource_bounds", required=True
    )


class DeprecatedInvokeTransactionSchema(DeprecatedTransactionSchema):
    contract_address = Felt(data_key="contract_address", load_default=None)
    sender_address = Felt(data_key="sender_address", load_default=None)
    entry_point_selector = Felt(data_key="entry_point_selector", load_default=None)
    calldata = fields.List(Felt(), data_key="calldata", required=True)
    nonce = Felt(data_key="nonce", load_default=None)

    @post_load
    def make_transaction(self, data, **kwargs) -> InvokeTransaction:
        _replace_invoke_contract_address_with_sender_address(data)
        return InvokeTransaction(**data)


class InvokeTransactionV3Schema(TransactionV3Schema):
    sender_address = Felt(data_key="sender_address", required=True)
    calldata = fields.List(Felt(), data_key="calldata", required=True)
    account_deployment_data = fields.List(
        Felt(), data_key="account_deployment_data", load_default=[]
    )
    nonce = Felt(data_key="nonce", required=True)

    @post_load
    def make_transaction(self, data, **kwargs) -> InvokeTransactionV3:
        return InvokeTransactionV3(**data)


class DeprecatedDeclareTransactionSchema(DeprecatedTransactionSchema):
    class_hash = Felt(data_key="class_hash", required=True)
    sender_address = Felt(data_key="sender_address", required=True)
    nonce = Felt(data_key="nonce", load_default=None)
    compiled_class_hash = Felt(data_key="compiled_class_hash", load_default=None)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclareTransaction:
        return DeclareTransaction(**data)


class DeclareTransactionV3Schema(TransactionV3Schema):
    class_hash = Felt(data_key="class_hash", required=True)
    compiled_class_hash = Felt(data_key="compiled_class_hash", load_default=None)
    nonce = Felt(data_key="nonce", required=True)
    sender_address = Felt(data_key="sender_address", required=True)
    account_deployment_data = fields.List(
        Felt(), data_key="account_deployment_data", load_default=[]
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclareTransactionV3:
        return DeclareTransactionV3(**data)


class DeployTransactionSchema(TransactionSchema):
    contract_address_salt = Felt(data_key="contract_address_salt", required=True)
    constructor_calldata = fields.List(
        Felt(), data_key="constructor_calldata", required=True
    )
    class_hash = Felt(data_key="class_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployTransaction:
        return DeployTransaction(**data)


class DeprecatedDeployAccountTransactionSchema(DeprecatedTransactionSchema):
    contract_address_salt = Felt(data_key="contract_address_salt", required=True)
    constructor_calldata = fields.List(
        Felt(), data_key="constructor_calldata", required=True
    )
    class_hash = Felt(data_key="class_hash", required=True)
    nonce = Felt(data_key="nonce", load_default=None)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployAccountTransaction:
        return DeployAccountTransaction(**data)


class DeployAccountTransactionV3Schema(TransactionV3Schema):
    contract_address_salt = Felt(data_key="contract_address_salt", required=True)
    constructor_calldata = fields.List(
        Felt(), data_key="constructor_calldata", required=True
    )
    class_hash = Felt(data_key="class_hash", required=True)
    nonce = Felt(data_key="nonce", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployAccountTransactionV3:
        return DeployAccountTransactionV3(**data)


class DeclareTransactionSchema(OneOfSchema):
    type_schemas = {
        0: DeprecatedDeclareTransactionSchema,
        1: DeprecatedDeclareTransactionSchema,
        2: DeprecatedDeclareTransactionSchema,
        3: DeclareTransactionV3Schema,
    }

    def get_data_type(self, data):
        return _extract_tx_version(data.get("version"))


class InvokeTransactionSchema(OneOfSchema):
    type_schemas = {
        0: DeprecatedInvokeTransactionSchema,
        1: DeprecatedInvokeTransactionSchema,
        3: InvokeTransactionV3Schema,
    }

    def get_data_type(self, data):
        return _extract_tx_version(data.get("version"))


class DeployAccountTransactionSchema(OneOfSchema):
    type_schemas = {
        1: DeprecatedDeployAccountTransactionSchema,
        3: DeployAccountTransactionV3Schema,
    }

    def get_data_type(self, data):
        return _extract_tx_version(data.get("version"))


class L1HandlerTransactionSchema(TransactionSchema):
    contract_address = Felt(data_key="contract_address", required=True)
    calldata = fields.List(Felt(), data_key="calldata", required=True)
    entry_point_selector = Felt(data_key="entry_point_selector", required=True)
    nonce = NumberAsHex(data_key="nonce", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> L1HandlerTransaction:
        return L1HandlerTransaction(**data)


class TypesOfTransactionsSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {
        "INVOKE": InvokeTransactionSchema,
        "DECLARE": DeclareTransactionSchema,
        "DEPLOY": DeployTransactionSchema,
        "DEPLOY_ACCOUNT": DeployAccountTransactionSchema,
        "L1_HANDLER": L1HandlerTransactionSchema,
    }


class PendingStarknetBlockSchema(Schema):
    parent_block_hash = Felt(data_key="parent_hash", required=True)
    sequencer_address = Felt(data_key="sequencer_address", required=True)
    transactions = fields.List(
        fields.Nested(TypesOfTransactionsSchema(unknown=EXCLUDE)),
        data_key="transactions",
        required=True,
    )
    timestamp = fields.Integer(data_key="timestamp", required=True)
    l1_gas_price = fields.Nested(
        ResourcePriceSchema(), data_key="l1_gas_price", required=True
    )
    starknet_version = fields.String(data_key="starknet_version", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return PendingStarknetBlock(**data)


class StarknetBlockSchema(Schema):
    block_hash = Felt(data_key="block_hash", required=True)
    parent_block_hash = Felt(data_key="parent_hash", required=True)
    block_number = fields.Integer(data_key="block_number", required=True)
    sequencer_address = Felt(data_key="sequencer_address", required=True)
    status = BlockStatusField(data_key="status", required=True)
    root = NonPrefixedHex(data_key="new_root", required=True)
    transactions = fields.List(
        fields.Nested(TypesOfTransactionsSchema(unknown=EXCLUDE)),
        data_key="transactions",
        required=True,
    )
    timestamp = fields.Integer(data_key="timestamp", required=True)
    starknet_version = fields.String(data_key="starknet_version", required=True)
    l1_gas_price = fields.Nested(
        ResourcePriceSchema(), data_key="l1_gas_price", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> StarknetBlock:
        return StarknetBlock(**data)


class StarknetBlockWithTxHashesSchema(Schema):
    block_hash = Felt(data_key="block_hash", required=True)
    parent_block_hash = Felt(data_key="parent_hash", required=True)
    block_number = fields.Integer(data_key="block_number", required=True)
    sequencer_address = Felt(data_key="sequencer_address", required=True)
    status = BlockStatusField(data_key="status", required=True)
    root = NonPrefixedHex(data_key="new_root", required=True)
    transactions = fields.List(Felt(), data_key="transactions", required=True)
    timestamp = fields.Integer(data_key="timestamp", required=True)
    starknet_version = fields.String(data_key="starknet_version", required=True)
    l1_gas_price = fields.Nested(
        ResourcePriceSchema(), data_key="l1_gas_price", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> StarknetBlockWithTxHashes:
        return StarknetBlockWithTxHashes(**data)


class BlockHashAndNumberSchema(Schema):
    block_hash = Felt(data_key="block_hash", required=True)
    block_number = fields.Integer(data_key="block_number", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> BlockHashAndNumber:
        return BlockHashAndNumber(**data)


class SyncStatusSchema(Schema):
    starting_block_hash = Felt(data_key="starting_block_hash", required=True)
    starting_block_num = Felt(data_key="starting_block_num", required=True)
    current_block_hash = Felt(data_key="current_block_hash", required=True)
    current_block_num = Felt(data_key="current_block_num", required=True)
    highest_block_hash = Felt(data_key="highest_block_hash", required=True)
    highest_block_num = Felt(data_key="highest_block_num", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> SyncStatus:
        return SyncStatus(**data)


class PendingStarknetBlockWithTxHashesSchema(Schema):
    parent_block_hash = Felt(data_key="parent_hash", required=True)
    sequencer_address = Felt(data_key="sequencer_address", required=True)
    transactions = fields.List(Felt(), data_key="transactions", required=True)
    timestamp = fields.Integer(data_key="timestamp", required=True)
    starknet_version = fields.String(data_key="starknet_version", required=True)
    l1_gas_price = fields.Nested(
        ResourcePriceSchema(), data_key="l1_gas_price", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> PendingStarknetBlockWithTxHashes:
        return PendingStarknetBlockWithTxHashes(**data)


class StorageDiffSchema(Schema):
    address = Felt(data_key="address", required=True)
    storage_entries = fields.List(
        fields.Nested(StorageEntrySchema()),
        data_key="storage_entries",
        required=True,
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> StorageDiffItem:
        return StorageDiffItem(**data)


class ContractDiffSchema(Schema):
    address = Felt(data_key="address", required=True)
    contract_hash = Felt(data_key="contract_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployedContract:
        return DeployedContract(**data)


class DeclaredContractHashSchema(Schema):
    class_hash = Felt(data_key="class_hash", required=True)
    compiled_class_hash = Felt(data_key="compiled_class_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclaredContractHash:
        return DeclaredContractHash(**data)


class DeployedContractSchema(Schema):
    address = Felt(data_key="address", required=True)
    class_hash = NonPrefixedHex(data_key="class_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return DeployedContract(**data)


class ContractsNonceSchema(Schema):
    contract_address = Felt(data_key="contract_address", required=True)
    nonce = Felt(data_key="nonce", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return ContractsNonce(**data)


class ReplacedClassSchema(Schema):
    contract_address = Felt(data_key="contract_address", required=True)
    class_hash = Felt(data_key="class_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> ReplacedClass:
        return ReplacedClass(**data)


class StateDiffSchema(Schema):
    storage_diffs = fields.List(
        fields.Nested(StorageDiffSchema()),
        data_key="storage_diffs",
        required=True,
    )
    deprecated_declared_classes = fields.List(
        Felt(),
        data_key="deprecated_declared_classes",
        required=True,
    )
    declared_classes = fields.List(
        fields.Nested(DeclaredContractHashSchema()),
        data_key="declared_classes",
        required=True,
    )
    deployed_contracts = fields.List(
        fields.Nested(DeployedContractSchema()),
        data_key="deployed_contracts",
        required=True,
    )
    replaced_classes = fields.List(
        fields.Nested(ReplacedClassSchema()),
        data_key="replaced_classes",
        required=True,
    )
    nonces = fields.List(
        fields.Nested(ContractsNonceSchema()), data_key="nonces", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> StateDiff:
        return StateDiff(**data)


class BlockStateUpdateSchema(Schema):
    block_hash = Felt(data_key="block_hash", required=True)
    new_root = Felt(data_key="new_root", required=True)
    old_root = Felt(data_key="old_root", required=True)
    state_diff = fields.Nested(StateDiffSchema(), data_key="state_diff", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> BlockStateUpdate:
        return BlockStateUpdate(**data)


class PendingBlockStateUpdateSchema(Schema):
    old_root = Felt(data_key="old_root", required=True)
    state_diff = fields.Nested(StateDiffSchema(), data_key="state_diff", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> PendingBlockStateUpdate:
        return PendingBlockStateUpdate(**data)


class SierraEntryPointSchema(Schema):
    selector = Felt(data_key="selector", required=True)
    function_idx = fields.Integer(data_key="function_idx", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> SierraEntryPoint:
        return SierraEntryPoint(**data)


class EntryPointSchema(Schema):
    offset = NumberAsHex(data_key="offset", required=True)
    selector = Felt(data_key="selector", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> EntryPoint:
        return EntryPoint(**data)


class SierraEntryPointsByTypeSchema(Schema):
    constructor = fields.List(
        fields.Nested(SierraEntryPointSchema()), data_key="CONSTRUCTOR", required=True
    )
    external = fields.List(
        fields.Nested(SierraEntryPointSchema()), data_key="EXTERNAL", required=True
    )
    l1_handler = fields.List(
        fields.Nested(SierraEntryPointSchema()), data_key="L1_HANDLER", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> SierraEntryPointsByType:
        return SierraEntryPointsByType(**data)


class EntryPointsByTypeSchema(Schema):
    constructor = fields.List(
        fields.Nested(EntryPointSchema()), data_key="CONSTRUCTOR", required=True
    )
    external = fields.List(
        fields.Nested(EntryPointSchema()), data_key="EXTERNAL", required=True
    )
    l1_handler = fields.List(
        fields.Nested(EntryPointSchema()), data_key="L1_HANDLER", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> EntryPointsByType:
        return EntryPointsByType(**data)


class SierraContractClassSchema(Schema):
    sierra_program = fields.List(Felt(), data_key="sierra_program", required=True)
    contract_class_version = fields.String(
        data_key="contract_class_version", required=True
    )
    entry_points_by_type = fields.Nested(
        SierraEntryPointsByTypeSchema(), data_key="entry_points_by_type", required=True
    )
    abi = fields.String(data_key="abi", required=False)

    @post_load
    def make_dataclass(self, data, **kwargs) -> SierraContractClass:
        return SierraContractClass(**data)


class ContractClassSchema(Schema):
    program = fields.String(data_key="program", required=True)
    entry_points_by_type = fields.Nested(
        EntryPointsByTypeSchema(), data_key="entry_points_by_type", required=True
    )
    abi = fields.List(
        fields.Nested(ContractAbiEntrySchema(unknown=EXCLUDE)), data_key="abi"
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> ContractClass:
        return ContractClass(**data)


class SentTransactionSchema(Schema):
    transaction_hash = Felt(data_key="transaction_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> SentTransactionResponse:
        return SentTransactionResponse(**data)


class DeclareTransactionResponseSchema(SentTransactionSchema):
    class_hash = Felt(data_key="class_hash", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclareTransactionResponse:
        return DeclareTransactionResponse(**data)


class DeployAccountTransactionResponseSchema(SentTransactionSchema):
    address = Felt(data_key="contract_address", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployAccountTransactionResponse:
        return DeployAccountTransactionResponse(**data)


# ------------------------------- Trace API -------------------------------


class OrderedEventSchema(Schema):
    keys = fields.List(Felt(), data_key="keys", required=True)
    data = fields.List(Felt(), data_key="data", required=True)
    order = fields.Integer(data_key="order", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs):
        return OrderedEvent(**data)


class OrderedMessageSchema(Schema):
    l2_address = Felt(data_key="from_address", required=True)
    l1_address = Felt(data_key="to_address", required=True)
    payload = fields.List(Felt(), data_key="payload", required=True)
    order = fields.Integer(data_key="order", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> OrderedMessage:
        return OrderedMessage(**data)


class FunctionInvocationSchema(Schema):
    contract_address = Felt(data_key="contract_address", required=True)
    entry_point_selector = Felt(data_key="entry_point_selector", required=True)
    calldata = fields.List(Felt(), data_key="calldata", required=True)
    caller_address = Felt(data_key="caller_address", required=True)
    class_hash = Felt(data_key="class_hash", required=True)
    entry_point_type = EntryPointTypeField(data_key="entry_point_type", required=True)
    call_type = CallTypeField(data_key="call_type", required=True)
    result = fields.List(Felt(), data_key="result", required=True)
    # https://marshmallow.readthedocs.io/en/stable/nesting.html#nesting-a-schema-within-itself
    calls = fields.List(
        fields.Nested(
            lambda: FunctionInvocationSchema()  # pylint: disable=unnecessary-lambda
        ),
        data_key="calls",
        required=True,
    )
    events = fields.List(
        fields.Nested(OrderedEventSchema()), data_key="events", required=True
    )
    messages = fields.List(
        fields.Nested(L2toL1MessageSchema()), data_key="messages", required=True
    )
    execution_resources = fields.Nested(
        ExecutionResourcesSchema(), data_key="execution_resources", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> FunctionInvocation:
        return FunctionInvocation(**data)


class RevertedFunctionInvocationSchema(Schema):
    revert_reason = fields.String(data_key="revert_reason", required=True)

    @post_load
    def make_dataclass(self, data, **kwargs) -> RevertedFunctionInvocation:
        return RevertedFunctionInvocation(**data)


class ExecuteInvocationSchema(OneOfSchema):
    type_schemas = {
        "REVERTED": RevertedFunctionInvocationSchema(),
        "FUNCTION_INVOCATION": FunctionInvocationSchema(),
    }

    def get_data_type(self, data):
        if "revert_reason" in data:
            return "REVERTED"
        return "FUNCTION_INVOCATION"


class InvokeTransactionTraceSchema(Schema):
    execute_invocation = fields.Nested(
        ExecuteInvocationSchema(), data_key="execute_invocation", required=True
    )
    validate_invocation = fields.Nested(
        FunctionInvocationSchema(), data_key="validate_invocation", load_default=None
    )
    fee_transfer_invocation = fields.Nested(
        FunctionInvocationSchema(),
        data_key="fee_transfer_invocation",
        load_default=None,
    )
    state_diff = fields.Nested(
        StateDiffSchema(), data_key="state_diff", load_default=None
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> InvokeTransactionTrace:
        return InvokeTransactionTrace(**data)


class DeclareTransactionTraceSchema(Schema):
    validate_invocation = fields.Nested(
        FunctionInvocationSchema(), data_key="validate_invocation", load_default=None
    )
    fee_transfer_invocation = fields.Nested(
        FunctionInvocationSchema(),
        data_key="fee_transfer_invocation",
        load_default=None,
    )
    state_diff = fields.Nested(
        StateDiffSchema(), data_key="state_diff", load_default=None
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeclareTransactionTrace:
        return DeclareTransactionTrace(**data)


class DeployAccountTransactionTraceSchema(Schema):
    constructor_invocation = fields.Nested(
        FunctionInvocationSchema(), data_key="constructor_invocation", required=True
    )
    validate_invocation = fields.Nested(
        FunctionInvocationSchema(), data_key="validate_invocation", load_default=None
    )
    fee_transfer_invocation = fields.Nested(
        FunctionInvocationSchema(),
        data_key="fee_transfer_invocation",
        load_default=None,
    )
    state_diff = fields.Nested(
        StateDiffSchema(), data_key="state_diff", load_default=None
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> DeployAccountTransactionTrace:
        return DeployAccountTransactionTrace(**data)


class L1HandlerTransactionTraceSchema(Schema):
    function_invocation = fields.Nested(
        FunctionInvocationSchema(), data_key="function_invocation", required=True
    )
    state_diff = fields.Nested(
        StateDiffSchema(), data_key="state_diff", load_default=None
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> L1HandlerTransactionTrace:
        return L1HandlerTransactionTrace(**data)


class TransactionTraceSchema(OneOfSchema):
    type_schemas = {
        "INVOKE": InvokeTransactionTraceSchema(),
        "DECLARE": DeclareTransactionTraceSchema(),
        "DEPLOY_ACCOUNT": DeployAccountTransactionTraceSchema(),
        "L1_HANDLER": L1HandlerTransactionTraceSchema(),
    }

    def get_data_type(self, data):
        return data["type"]


class SimulatedTransactionSchema(Schema):
    # `unknown=EXCLUDE` in order to skip `type=...` field we don't want
    transaction_trace = fields.Nested(
        TransactionTraceSchema(),
        data_key="transaction_trace",
        required=True,
        unknown=EXCLUDE,
    )
    fee_estimation = fields.Nested(
        EstimatedFeeSchema(), data_key="fee_estimation", required=True
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> SimulatedTransaction:
        return SimulatedTransaction(**data)


class BlockTransactionTraceSchema(Schema):
    transaction_hash = Felt(data_key="transaction_hash", required=True)
    # `unknown=EXCLUDE` in order to skip `type=...` field we don't want
    trace_root = fields.Nested(
        TransactionTraceSchema(), data_key="trace_root", required=True, unknown=EXCLUDE
    )

    @post_load
    def make_dataclass(self, data, **kwargs) -> BlockTransactionTrace:
        return BlockTransactionTrace(**data)
