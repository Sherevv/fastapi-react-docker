import { useShow, IResourceComponentsProps } from "@pankod/refine-core";
import { Show, Typography, RefreshButton } from "@pankod/refine-antd";

import { IPortfolio } from "interfaces";

const { Title, Text } = Typography;

export const PortfolioShow: React.FC<IResourceComponentsProps> = () => {
    const { queryResult } = useShow<IPortfolio>({
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