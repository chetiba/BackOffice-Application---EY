using System;

namespace ClaimsManagement.Models
{
    using System;
    using System.Text.Json.Serialization;

    public class Claim
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public DateTime DateSubmitted { get; set; }

        [JsonPropertyName("reclamationType")]
        public ReclamationType TypeOfReclamation { get; set; }

        [JsonPropertyName("reclamationStatus")]
        public ReclamationStatus Status { get; set; }
    }

    public enum ReclamationType
    {
        VirtualAgent, Dashboard, Mission, Collaborateur, Stagiaire, Client
    }

    public enum ReclamationStatus
    {
        Pending, Done
    }
}