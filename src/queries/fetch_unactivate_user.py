from gql import gql

query = gql("""
    query fetchUnactivateUser(
        $where: users_bool_exp
    ) {
        users(
            where: $where
        ) {
            id
        }
    }
""")