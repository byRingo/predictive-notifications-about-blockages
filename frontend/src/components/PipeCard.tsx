import styled from "styled-components";
import pipe from '../assets/pipe.png'

interface PipeCardProps{
    label: string,
    blockage: number,
}


const Card = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    height: 18rem;
    padding: 3rem;
    border-radius: 1rem;
`

const Title = styled.span`
text-align: center;
    font-size: 1.2rem;
    margin-top: -1.5rem;
`

const Description = styled.span`
    text-align: center;
`

export default function PipeCard({label, blockage, }: PipeCardProps){
    return(<Card>
        <Title>{label}</Title>
        <img src={pipe} alt=""/>
        <Description>Засор: {blockage}</Description>
        <Description>Проверка: 01.01.2024</Description>
    </Card>)
}