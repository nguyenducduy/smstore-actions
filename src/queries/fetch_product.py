from gql import gql

query = gql("""
    query fetchProduct(
        $id: Int!
    ) {
        products_by_pk(
            id: $id
        ) {
            id
            category_id
            name
            slug
            is_active
            in_stock
            price
            images(limit: 1) {
                id
                path
            }
        }
    }
""")