import pipe from '../../assets/pipe.png'
import styled from 'styled-components';
import { Card, Description, Title } from "./PipeCardStyles.ts";

interface PipeCardProps {
    label: string,
    blockage: number,
}

export const PipeImg = styled.img`
    width:140px;
    margin-left:auto;
    margin-right:auto
`

export default function PipeCard({label, blockage, }: PipeCardProps){
    return(<Card $blockage={blockage}>
        <Title>{label}</Title>
        <PipeImg src={pipe} alt="" />
        <Description>Засор: {blockage}</Description>
        <Description>Проверка: 01.01.2024</Description>
    </Card>)
}