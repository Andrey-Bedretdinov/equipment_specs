import { Typography } from "antd";
import { useGetProjectsQuery } from "../../redux/services/projectsApi"
import ProjectCard from "../ProjectCard/ProjectCard";
import Loader from "../Loader/Loader";

const { Title } = Typography;

const ProjectCardsList = () => {

    const { data, isLoading, isError } = useGetProjectsQuery();

    return (
        <>
            <Title level={2} >Список проектов</Title>

            <Loader isLoading={isLoading} isError={isError}/>

            {data?.map((project) =>
                <ProjectCard key={project.id} project={project} />
            )}
        </>
    )
}

export default ProjectCardsList;