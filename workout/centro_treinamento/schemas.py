from typing import Annotated
from pydantic import Field
from workout.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Av. das Nações Unidas, 1000', max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do proprietário', example='Daniel', max_length=30)]

class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]