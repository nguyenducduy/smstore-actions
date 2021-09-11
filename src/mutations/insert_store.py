from gql import gql

query = gql("""
    mutation insertStore(
        $object: stores_insert_input!
    ) {
        insert_stores_one(
            object: $object
        ) {
            id
        }
    }
""")