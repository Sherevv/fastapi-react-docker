import { useForm, Form, Input, Edit, RefreshButton, ListButton } from "@pankod/refine-antd";
import { IBroker } from "interfaces";
import { HttpError } from "@pankod/refine-core";
import { Space } from "antd";
import React from "react";

export const BrokerEdit: React.FC = () => {
    const { formProps, saveButtonProps, queryResult } = useForm<IBroker,
        HttpError,
        IBroker>({
        metaData:{
            fields: [
                "id",
                "name",
            ],
        },

    });
    const postData = queryResult?.data?.data;

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
                      </Space>  }}
        >
            <Form {...formProps} layout="vertical">
                <Form.Item label="Name" name="name"
                           rules={[
                    {
                        required: true,
                    },
                ]}>
                    <Input />
                </Form.Item>
            </Form>
        </Edit>
    );
};