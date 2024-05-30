import logo from "./assets/logo.png"
import styled from "styled-components";
import PipeCard from "./components/PipeCard.tsx";

function App() {

    const cardsArray = [{label: "1 подъезд",
    blockage: 12},{label: "2 подъезд",
        blockage: 31},{label: "3 подъезд",
        blockage: 34},{label: "4 подъезд",
        blockage: 87}]

  const Logo = styled.img`
        width: 64px;
        margin: 1rem;
    `

  const CompanyName = styled.span`
      font-weight: 700;
      font-size: 1.5rem;
  `

  const Main = styled.main`
    flex-grow: 1;
    background-color: #EAEAEA;
  `

  const Footer = styled.div`
    display: flex;
      background-color:#C9C9C9;
    height: 70px;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
  `

  const Header = styled.div`
    display: flex;
    height: 100px;
    background-color: #C9C9C9;
    gap: 2rem;
    align-items: center;
  `

  const ResidentialComplexSection = styled.section`
    display: flex;
    flex-direction: column;
    margin: 1rem;
  `

  const Body = styled.div`
  display: flex;
  flex-direction: column;
    min-height: 100vh;
  `

    const CardSection = styled.section`
    display: flex;
        gap: 2rem;
    justify-content: center;    
    `

  return (
    <Body>
      <Header>
          <Logo src={logo} alt={"logo"} />
          <CompanyName>Company name</CompanyName>
      </Header>
      <Main>
        <ResidentialComplexSection>
          <p>Адрес дома</p>
          <p>ул. Сибирская 7, д.2</p>
        </ResidentialComplexSection>
          <CardSection>
              {cardsArray.map(cur => {
                  return (<PipeCard label={cur.label} blockage={cur.blockage}></PipeCard>)
              })}
          </CardSection>
      </Main>
      <Footer>
        <span>Большой бушизм</span>
      </Footer>
    </Body>
  )
}

export default App
