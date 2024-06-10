from fastapi import APIRouter, Body, status, HTTPException
from workout.categorias.schemas import CategoriaIn, CategoriaOut
from workout.contrib.dependencies import DatabaseDependency
from uuid import uuid4
from workout.categorias.models import CategoriaModel
from sqlalchemy.future import select
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError


router = APIRouter()

@router.post(path='/', 
    summary='Criar nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut
    )
async def post(
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:

    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    try:
        db_session.add(categoria_model)
        await db_session.commit()
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe categoria com o nome: {categoria_model.nome}')
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Ocorreu um erro ao inserir os dados.'
            )

    
    return categoria_out
    
@router.get(path='/',
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut])
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(
        select(CategoriaModel))
    ).scalars().all()

    return categorias

@router.get(path='/{id}',
    summary='Consultar uma categoria pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut)
async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(
        select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma categoria encontrada com o ID fornecido",
        )

    return categoria