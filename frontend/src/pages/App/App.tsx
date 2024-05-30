import logo from "../../assets/logo_test.png"
import PipeCard from "../../components/PipeCard/PipeCard.tsx";
import {Body, CardSection, HomeAddress, Logo, Main, ResidentialComplexSection} from "./AppStyles.ts";
import Header from "../../components/Header/Header.tsx";
import {CompanyName} from "../../components/Header/HeaderStyles.ts";
import Footer from "../../components/Footer/Footer.tsx";

export default function App() {

    const cardsArray = [{label: "1 подъезд",
        blockage: 12},{label: "2 подъезд",
        blockage: 31},{label: "3 подъезд",
        blockage: 52},{label: "4 подъезд",
        blockage: 10}]

  return (
    <Body>
      <Header>
          <Logo src={logo} alt={"logo"} />
          <CompanyName>Большой бушизм</CompanyName>
      </Header>
      <Main>
        <ResidentialComplexSection>
          <HomeAddress>ул. Сибирская 7, д.2</HomeAddress>
        </ResidentialComplexSection>
        <CardSection>
          {cardsArray.map(cur => {
            return (<PipeCard label={cur.label} blockage={cur.blockage}></PipeCard>)
          })}
        </CardSection>
      </Main>
      <Footer>
        <span>Предикативные уведомления о протечках/засорах</span>
      </Footer>
    </Body>
  )
}
