import { useShow, useOne, IResourceComponentsProps } from "@pankod/refine-core";
import { Show, Typography, Tag, RefreshButton } from "@pankod/refine-antd";

import { IBroker, IPortfolio } from "interfaces";
import { useParams } from "react-router-dom";

const { Title, Text } = Typography;

export const PortfolioShow: React.FC<IResourceComponentsProps> = () => {
    const { action, id } = useParams();
    const { queryResult } = useShow<IPortfolio>({
        id: id,
        metaData:{
                fields: [
                    "id",
                    "name",
                    {
                        broker: [
                            "name"
                        ],
                    },
                ],
            },
        }
    );
    const { data, isLoading } = queryResult;
    const record = data?.data;

    return (
        <Show isLoading={isLoading}
              pageHeaderProps={{ extra: <RefreshButton onClick={() => queryResult.refetch()} /> }}>
            <Title level={5}>Id</Title>
            <Text>{record?.id}</Text>

            <Title level={5}>Name</Title>
            <Text>{record?.name}</Text>

            <Title level={5}>Broker</Title>
            <Text>{record?.broker?.name}</Text>
        </Show>
    );
};