from gql import gql

query = gql("""
    mutation updateUserField(
        $id: Int!
        $fields: users_set_input
    ) {
        update_users(
            where: {
                id: { _eq: $id }
            },
            _set: $fields
        ) {
            affected_rows
        } 
    }
""")