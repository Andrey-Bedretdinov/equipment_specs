import React from "react";
import { Card, Typography } from "antd";
import type { IProject } from "../../types/types";
import { useNavigate } from "react-router-dom";

const { Text } = Typography

interface ProjectCardProps {
    project: IProject
}

const ProjectCard: React.FC<ProjectCardProps> = ({project}) => {

    const navigate = useNavigate();
    
    return (
        <Card
            hoverable
            onClick={() => navigate(`/projects/${project.id}`)}
            title={
                <Text strong>{project.name}</Text>
            }
        >
            <Text>{project.description}</Text>
        </Card>
    )
}

export default ProjectCard;