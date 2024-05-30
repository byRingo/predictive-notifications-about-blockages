import styled from "styled-components";

export const Card = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    height: 18rem;
    padding: 3rem;
    border-radius: 1rem;
    border: 1px solid rgb(180 180 180);
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
`

export const Title = styled.span`
text-align: center;
    font-size: 1.2rem;
    margin-top: -1.5rem;
`

export const Description = styled.span`
    text-align: center;
`