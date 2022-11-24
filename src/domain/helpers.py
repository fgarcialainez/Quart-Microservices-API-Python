from pydantic import BaseModel
from sqlalchemy.engine import ScalarResult


def row_to_dict_list(row_list: ScalarResult) -> [dict]:
    return [row.as_dict() for row in row_list]


def row_to_model_list(row_list: ScalarResult, model: type(BaseModel)) -> [BaseModel]:
    return [model.parse_obj(row.as_dict()) for row in row_list]


def dict_to_model_list(dict_list: [dict], model: type(BaseModel)) -> [BaseModel]:
    return [model.parse_obj(item) for item in dict_list]


def model_to_dict_list(model_list: [BaseModel]) -> [dict]:
    return [model.dict() for model in model_list]
