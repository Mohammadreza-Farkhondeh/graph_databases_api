from fastapi import APIRouter

router = APIRouter()


@router.post("/databases")
def databases(request):
    """
    X-HOST AND X-PORT should be in headers
    username and password
    :return:
    list of database in host
    """
    databases = re