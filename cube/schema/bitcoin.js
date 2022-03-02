cube(`Bitcoin`, {
  sql: `SELECT * FROM dw_crypto.fct_transactions`,

  measures: {
    transactionSize: {
      type: `sum`,
      sql: `transactions.size`
    },
    transactionVirtualSize: {
      type: `sum`,
      sql: `transactions.virtual_size`
    },
    transactionFee: {
      type: `sum`,
      sql: `transactions.fee`
    },
    transactionCount: {
      type: `sum`,
      sql: `blocks.transaction_count`
    },
  },

  dimensions: {
    transactionVersion: {
      type: `number`,
      sql: `transactions.version`,
    },
    isTransactionCoinbase: {
      type: `boolean`,
      sql: `transactions.is_coinbase`,
    },
    blockTimestamp: {
      type: `time`,
      sql: `blocks.timestamp`,
    },
  },
});