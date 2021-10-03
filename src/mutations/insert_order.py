from gql import gql

query = gql("""
    mutation insertOrder(
        $object: orders_insert_input!
    ) {
        insert_orders_one(
            object: $object
        ) {
            id
        }
    }
""")