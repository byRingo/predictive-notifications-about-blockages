import styled from "styled-components";

export const Logo = styled.img`
        width: 64px;
        margin: 1rem;
    `

export const Main = styled.main`
    flex-grow: 1;
    background-color: rgb(240 240 240);
    display: flex;
    flex-direction: column;
  `

export const ResidentialComplexSection = styled.section`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 75%;
    margin-left: auto;
    margin-right: auto;
  `

export const Body = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  `

export const CardSection = styled.section`
    flex-wrap: wrap;
    display: flex;
        gap: 2rem;
    justify-content: center;    
    `

export const HomeAddress = styled.p`
        font-weight: 550;
        font-size: 1.3rem;
        background-color: white;
        padding: 1rem;
    border-radius: 1rem;
    `