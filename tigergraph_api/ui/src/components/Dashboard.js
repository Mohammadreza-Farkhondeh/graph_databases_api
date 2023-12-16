import React, {useEffect, useState} from "react";
import api from "../Api";
import {Button, Form, Input, Modal, Select} from "antd";
import Data, { useData } from "./Data";

function Dashboard() {
  const [visible, setVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();
  const [, setData] = useData();

  useEffect(() => {
    async function fetchSchema () {
      try {
        return await api.get("/graph/schema")
      } catch (error) {
        console.error(error);
      }
    }
    fetchSchema().then(response => setData(response.data));
  });

  const showModal = () => {
    setVisible(true);
  };

  const hideModal = () => {
    setVisible(false);
  };

  const submitForm = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      switch (values.action) {
        case "edge_upsert":
          await api.post("/edges/", values.data).then(handleResponse).catch(handleError);
          break;
        case "edge_retrieve":
          await api.get("/edges/", { params: values.data }).then(handleResponse).catch(handleError);
          break;
        case "edge_delete":
          await api.delete("/edges/", { params: values.data }).then(handleResponse).catch(handleError);
          break;
        case "vertex_upsert":
          await api.post("/vertices/", { params: values.data }).then(handleResponse).catch(handleError);
          break;
        case "vertex_retrieve":
          await api.get("/vertices/", { params: values.data }).then(handleResponse).catch(handleError);
          break;
        case "vertex_delete":
          await api.delete("/vertices/", { params: values.data }).then(handleResponse).catch(handleError);
          break;
        case "upsert_data":
          await api.post("/graph/upsert", { params: values.data }).then(handleResponse).catch(handleError);
          break;
        default:
          console.log("Unknown action");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleResponse = (response) => {
    setLoading(false);
    hideModal();
    setData(response.data);
  };

  const handleError = (error) => {
    setLoading(false);
    hideModal();
    console.error(error);
  };

  return (
    <div className="Dashboard">
      <h1>TigerGraph DASHBOARD</h1>
      <Button type="primary" onClick={showModal}>
        Make a request
      </Button>
      <Modal
        title="Request Form"
        open={visible}
        confirmLoading={loading}
        onOk={submitForm}
        onCancel={hideModal}
        okText="Submit"
        cancelText="Cancel"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="action" label="Select an action" rules={[{ required: true }]}>
            <Select placeholder="Please select an action">
              <Select.Option value="edge_upsert">Edge Upsert</Select.Option>
              <Select.Option value="edge_retrieve">Edge Retrieve</Select.Option>
              <Select.Option value="edge_delete">Edge Delete</Select.Option>
              <Select.Option value="vertex_upsert">Vertex Upsert</Select.Option>
              <Select.Option value="vertex_retrieve">Vertex Retrieve</Select.Option>
              <Select.Option value="vertex_delete">Vertex Delete</Select.Option>
              <Select.Option value="upsert_data">Upsert Data</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="data" label="Enter the data" rules={[{ required: true }]}>
            <Input.TextArea placeholder="Please enter the data in JSON format" />
          </Form.Item>
        </Form>
      </Modal>
      <Data />
    </div>
  );
}

export default Dashboard;
