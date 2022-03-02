SELECT
    (SELECT AS STRUCT transactions.*) AS transactions,
    (SELECT AS STRUCT blocks.*) AS blocks,
FROM
    {{ source('crypto_bitcoin', 'transactions') }} transactions
INNER JOIN
    {{ source('crypto_bitcoin', 'blocks') }} blocks
ON
    transactions.block_hash = blocks.hash
WHERE
    # Get data from "2022-01-01" to "2022-01-31"
    block_timestamp_month = "2022-01-01"
    AND timestamp_month = "2022-01-01"