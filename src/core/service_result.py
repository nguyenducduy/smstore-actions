from loguru import logger
import inspect
from gql import Client as GraphqlClient
from config.graphql_client import transport
from utils.app_exceptions import AppExceptionCase

from mutations.insert_error_logs import query as insertErrorLogs


class ServiceResult(object):
    def __init__(self, arg):
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
        self.value = arg

    def __str__(self):
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")

            if result.exception_case in [
                'EventTriggerFail',
                'SyncToEsFail',
                'CreateMediaFail',
                'UpdateMediaFail',
                'FetchAudioFail',
                'CreateEpisodeFail',
                'UpdateEpisodeFail',
                'AddFavoriteFail',
                'RemoveFavoriteFail',
                'SubcribeFail',
                'UnsubcribeFail',
                'AddFcmFail'
            ]:
                graphqlClient = GraphqlClient(
                    transport=transport,
                    fetch_schema_from_transport=True
                )
                graphqlClient.execute(insertErrorLogs, variable_values={
                    'object': {
                        'class_exception_name': str(result.exception_case),
                        'caller': str(caller_info()),
                        'message': str(exception)
                    }
                })
                
            raise exception
    with result as result:
        return result
