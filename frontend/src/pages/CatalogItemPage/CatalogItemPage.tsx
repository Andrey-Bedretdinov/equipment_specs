import { Typography } from "antd";
import { useGetCatalogItemsQuery } from "../../redux/services/catalogApi";
import Loader from "../../components/Loader/Loader";
import ItemCardsList from "../../components/ItemCardsList/ItemCardsList";

const { Title } = Typography;

const CatalogItemPage: React.FC = () => {

    const { data: items_list, isLoading, isError } = useGetCatalogItemsQuery();

    return (
        <>
            <Title>Каталог Items</Title>

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <ItemCardsList items_list={items_list ?? []} />
            )}
        </>
    );
}

export default CatalogItemPage;