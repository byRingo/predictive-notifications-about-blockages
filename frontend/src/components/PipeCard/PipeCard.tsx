import pipe from '../../assets/pipe.png'
import { Card, Description, Title } from "./PipeCardStyles.ts";

interface PipeCardProps {
    label: string,
    blockage: number,
}

export default function PipeCard({label, blockage, }: PipeCardProps){
    return(<Card $blockage={blockage}>
        <Title>{label}</Title>
        <img src={pipe} alt="" />
        <Description>Засор: {blockage}</Description>
        <Description>Проверка: 01.01.2024</Description>
    </Card>)
}