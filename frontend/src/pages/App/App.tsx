import logo from "../../assets/logo.png"
import PipeCard from "../../components/PipeCard/PipeCard.tsx";
import { Body, CardSection, HomeAddress, Logo, Main, ResidentialComplexSection } from "./AppStyles.ts";
import Header from "../../components/Header/Header.tsx";
import { CompanyName } from "../../components/Header/HeaderStyles.ts";
import Footer from "../../components/Footer/Footer.tsx";
import { useEffect, useState } from "react";
import { get_json } from "../../api/get_json.ts";
import { get_data } from "../../api/get_data.ts";

export type TPipe = {
  day: number,
  blockageChance: number
}

export default function App() {

  const [matilda, setMatilda] = useState<number[]>([])

  useEffect(() => {
    async function getData() {
      await get_json();
      const data = await get_data()
      setMatilda(Object.values(data))
    }
    getData();
  }, [])

  return (
    <Body>
      <Header>
        <Logo src={logo} alt={"logo"} />
        <CompanyName>ЖК Большой бушизм</CompanyName>
      </Header>
      <Main>
        <ResidentialComplexSection>
          <HomeAddress>Адрес дома: ул. Сибирская 7, д.2</HomeAddress>
        </ResidentialComplexSection>
        <CardSection>
          {matilda.map((cur, index) => {
            return (<PipeCard label={`Подъезд ${index + 1}`} blockage={Math.round(cur)} key={index}></PipeCard>)
          })}
        </CardSection>
      </Main>
      <Footer>
        <span>Предикативные уведомления о протечках/засорах</span>
      </Footer>
    </Body>
  )
}
