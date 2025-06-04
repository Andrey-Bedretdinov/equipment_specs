import { Typography } from "antd";
import { useGetCatalogKtsQuery } from "../../redux/services/catalogApi";
import Loader from "../../components/Loader/Loader";
import KtsCardsList from "../../components/KtsCardsList/KtsCardsList";

const { Title } = Typography;

const CatalogKtsPage: React.FC = () => {

    const { data: kts_list, isLoading, isError } = useGetCatalogKtsQuery();
    console.log(kts_list)

    return (
        <>
            <Title>Каталог KTC</Title>

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <KtsCardsList kts_list={kts_list ?? []}/>
            )}


        </>
    );
}

export default CatalogKtsPage;