using UnityEngine;
using ROS2;

public class UnityROSConnection : MonoBehaviour
{
    [Header("ROS Connection Settings")]
    public string rosIP = "127.0.0.1";
    public int rosPort = 8888;

    [Header("Robot Configuration")]
    public string robotNamespace = "humanoid_robot";

    private ROS2UnityComponent ros2Unity;
    private bool isConnected = false;

    void Start()
    {
        InitializeROSConnection();
    }

    private void InitializeROSConnection()
    {
        ros2Unity = GetComponent<ROS2UnityComponent>();
        if (ros2Unity != null)
        {
            ros2Unity.Init();
            ros2Unity.Connect(rosIP, rosPort);

            // Wait for connection
            InvokeRepeating("CheckConnection", 0.5f, 0.5f);
        }
        else
        {
            Debug.LogError("ROS2UnityComponent not found on this GameObject!");
        }
    }

    void CheckConnection()
    {
        if (ros2Unity != null && ros2Unity.Ok())
        {
            isConnected = true;
            Debug.Log("Connected to ROS 2!");
            CancelInvoke("CheckConnection");
        }
    }

    void OnDestroy()
    {
        if (ros2Unity != null && ros2Unity.Ok())
        {
            ros2Unity.Shutdown();
        }
    }

    public bool IsConnected()
    {
        return isConnected;
    }

    // Example method to publish joint states
    public void PublishJointState(string[] jointNames, float[] positions)
    {
        if (!IsConnected()) return;

        // Implementation would depend on the specific ROS2Unity library being used
        // This is a placeholder for the concept
        Debug.Log($"Publishing joint states for {jointNames.Length} joints");
    }
}