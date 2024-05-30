import pipe from '../../assets/pipe.png'
import {Card, Description, PipeImg, Title} from "./PipeCardStyles.ts";
import styled from "styled-components";

interface PipeCardProps {
    label: string,
    blockage: number,
}

const Text = styled.span`
  font-size: 18px;
`

export default function PipeCard({label, blockage, }: PipeCardProps){
    return(<Card $blockage={blockage}>
        <Title>{label}</Title>
        <PipeImg src={pipe} alt="" />

        <Description>
            <Text>Засор: {blockage}</Text>
        <Text>Проверка: 01.01.2024</Text>
        </Description>
    </Card>)
}