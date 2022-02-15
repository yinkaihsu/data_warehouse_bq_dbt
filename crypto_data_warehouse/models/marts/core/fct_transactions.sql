SELECT
    *
FROM
    {{ ref('stg_crypto_bitcoin__transactions_with_blocks') }}