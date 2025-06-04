import { Typography } from "antd";
import { useGetCatalogUnitsQuery } from "../../redux/services/catalogApi";
import Loader from "../../components/Loader/Loader";
import UnitCardsList from "../../components/UnitCardsList/UnitCardsList";

const { Title } = Typography;

const CatalogUnitPage: React.FC = () => {

    const { data: units_list, isLoading, isError } = useGetCatalogUnitsQuery();

    return (
        <>
            <Title>Каталог Units</Title>

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <UnitCardsList units_list={units_list ?? []}/>
            )}


        </>
    );
}

export default CatalogUnitPage;