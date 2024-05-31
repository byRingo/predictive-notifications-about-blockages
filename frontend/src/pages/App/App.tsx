import logo from "../../assets/logo.png"
import PipeCard from "../../components/PipeCard/PipeCard.tsx";
import { Body, CardSection, HomeAddress, Logo, Main, ResidentialComplexSection } from "./AppStyles.ts";
import Header from "../../components/Header/Header.tsx";
import { CompanyName } from "../../components/Header/HeaderStyles.ts";
import Footer from "../../components/Footer/Footer.tsx";
import { useEffect, useState } from "react";
import { get_json } from "../../api/get_json.ts";
import { get_data } from "../../api/get_data.ts";
import maintenanceInfo from "../../../../backend/maintenances.json";

export default function App() {

  const [pipes, setPipes] = useState<number[]>([])
  const [dates, setDates] = useState<string[]>([])

  useEffect(() => {
    async function getData() {
      await get_json();
      const data = await get_data()
      setPipes(Object.values(data))
    }
    getData().catch((err) => console.log(err));
    setDates(Object.values(maintenanceInfo))
  }, [])

  return (
    <Body>
      <Header>
        <Logo src={logo} alt={"logo"} />
        <CompanyName>Интерфейс УК</CompanyName>
      </Header>
      <Main>
        <ResidentialComplexSection>
          <HomeAddress>Адрес дома: ул. Адмирала Хакатонова, 8</HomeAddress>
        </ResidentialComplexSection>
        <CardSection>
          {pipes.map((cur, index) => {
            return (
              <PipeCard
                label={`Подъезд ${index + 1}`}
                blockage={Math.round(cur)}
                key={index}
                maintenance_date={dates[index]}>
              </PipeCard>
            )
          })}
        </CardSection>
      </Main>
      <Footer>
        <span>ЖК Большой бушизм ©️ 2024</span>
      </Footer>
    </Body>
  )
}
