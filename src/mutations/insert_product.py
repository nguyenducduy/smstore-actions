from gql import gql

query = gql("""
    mutation insertProduct(
        $object: products_insert_input!
    ) {
        insert_products_one(
            object: $object
        ) {
            id
        }
    }
""")