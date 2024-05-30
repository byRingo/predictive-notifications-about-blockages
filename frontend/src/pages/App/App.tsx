import logo from "../../assets/logo.png"
import PipeCard from "../../components/PipeCard/PipeCard.tsx";
import {Body, CardSection, CompanyName, Footer, Header, Logo, Main, ResidentialComplexSection} from "./AppStyles.ts";

export default function App() {

    const cardsArray = [{label: "1 подъезд",
        blockage: 12},{label: "2 подъезд",
        blockage: 31},{label: "3 подъезд",
        blockage: 34},{label: "4 подъезд",
        blockage: 87}]

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
