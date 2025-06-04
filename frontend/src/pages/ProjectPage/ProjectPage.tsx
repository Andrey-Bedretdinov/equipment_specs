import { useParams } from "react-router-dom";
import { useGetProjectByIdQuery } from "../../redux/services/projectsApi";
import Loader from "../../components/Loader/Loader";
import ItemCardsList from "../../components/ItemCardsList/ItemCardsList";

const ProjectPage: React.FC = () => {

    const { project_id } = useParams();
    const { data: project, isLoading, isError } = useGetProjectByIdQuery(project_id as string);

    return (
        <>
            Страница проекта {project_id}

            {(isLoading || isError) ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <ItemCardsList items_list={project?.items_list ?? []} />
            )}

        </>
    );
}

export default ProjectPage;