import { useParams } from "react-router-dom";
import { useGetProjectByIdQuery } from "../../redux/services/projectsApi";
import Loader from "../../components/Loader/Loader";
import ItemCardsList from "../../components/ItemCardsList/ItemCardsList";
import KtsCardsList from "../../components/KtsCardsList/KtsCardsList";
import { Card, Typography } from "antd";

const { Title, Text } = Typography;

const ProjectPage: React.FC = () => {

    const { project_id } = useParams();
    const { data: project, isLoading, isError } = useGetProjectByIdQuery(project_id as string);

    return (
        <Card
            title={
                <>
                    <Title>{project?.name}</Title>
                    <Text>{project?.description}</Text><br/>
                    <Text strong>Итоговая стоимость: {project?.price} ₽</Text>
                </>
            }
        >


            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <>
                    <KtsCardsList kts_list={project?.kts_list ?? []} />
                    <ItemCardsList items_list={project?.items_list ?? []} />
                </>
            )}
        </Card>
    );
}

export default ProjectPage;