from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from workout.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout.centro_treinamento.models import CentroTreinamentoModel
from workout.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post(path='/',summary='Criar novo centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id = uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    try:
        db_session.add(centro_treinamento_model)
        await db_session.commit()
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f'Ja existe um centro de treinamento com o nome: {centro_treinamento_model.nome}')
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Ocorreu um erro ao inserir os dados.'
            )

    return centro_treinamento_out

@router.get(
    '/', 
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento_out: list[CentroTreinamentoOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    
    return centros_treinamento_out


@router.get(
    '/{id}', 
    summary='Consulta um centro de treinamento pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )
    
    return centro_treinamento_out