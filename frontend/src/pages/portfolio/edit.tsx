import { useForm, Form, Input, Select, Edit, useSelect, RefreshButton, ListButton } from "@pankod/refine-antd";
import { IBroker, IPortfolio } from "interfaces";
import { useParams } from "react-router-dom";
import { HttpError } from "@pankod/refine-core";
import { Space } from "antd";
import React from "react";

export const PortfolioEdit: React.FC = () => {
    //let { action, id } = useParams();
    //let idd = id? id : '';
    const { formProps, saveButtonProps, queryResult } = useForm<IPortfolio,
        HttpError,
        IPortfolio>({
        //id: parseInt(idd),
        metaData:{
            fields: [
                "id",
                "name",
                {
                    broker: [
                        "id"
                    ],
                },
            ],
        },

    });

    const postData = queryResult?.data?.data;

    const { selectProps: brokerSelectProps } = useSelect<IBroker>({
        resource: "brokers",
        metaData:{
            fields: [
                "id",
                "name",
            ],
        },
        optionLabel: "name",
        optionValue: "id",
        defaultValue: postData?.broker?.id
    });



    return (
        <Edit saveButtonProps={saveButtonProps}
              pageHeaderProps={{ extra:
                  <Space wrap>
                      <ListButton />
                      <RefreshButton
                          onClick={() =>{
                              if(postData)  // hack to fire rerender
                                postData.name=''
                              queryResult?.refetch()
                          }}
                      />
                  </Space> }}
        >
            <Form {...formProps} layout="vertical"
                  onFinish={(values) =>
                      formProps.onFinish?.({
                          ...values,
                          broker: values.broker.id,
                      } as any)
                  }>
                <Form.Item label="Name" name="name"
                           rules={[
                    {
                        required: true,
                    },
                ]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Broker" name={["broker", "id"]}>
                    <Select {...brokerSelectProps} />
                </Form.Item>
            </Form>
        </Edit>
    );
}