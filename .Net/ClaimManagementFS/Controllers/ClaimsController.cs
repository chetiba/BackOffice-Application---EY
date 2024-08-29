using Microsoft.AspNetCore.Mvc;
using ClaimsManagement.Models;
using ClaimsManagement.Services;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using ClaimsManagement.Data;

namespace ClaimsManagement.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ClaimsController : ControllerBase
    {
        private readonly IClaimService _claimService;
        private readonly ApplicationDbContext _context;
        private readonly ILogger<ClaimsController> _logger;

        // Constructor with dependency injection
        public ClaimsController(IClaimService claimService, ApplicationDbContext context, ILogger<ClaimsController> logger)
        {
            _claimService = claimService;
            _context = context;
            _logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> GetAllClaims()
        {
            _logger.LogInformation("Fetching all claims");
            var claims = await _claimService.GetAllClaimsAsync();
            return Ok(claims);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetClaimById(int id)
        {
            _logger.LogInformation("Fetching claim with ID: {Id}", id);
            var claim = await _claimService.GetClaimByIdAsync(id);
            if (claim == null)
            {
                _logger.LogWarning("Claim with ID: {Id} not found", id);
                return NotFound();
            }
            return Ok(claim);
        }

        [HttpPost]
        public async Task<IActionResult> CreateClaim([FromBody] Claim claim)
        {
            _logger.LogInformation("Received claim data: {@Claim}", claim);

            if (claim == null)
            {
                return BadRequest("Claim data is missing.");
            }

            _context.Claims.Add(claim);
            await _context.SaveChangesAsync();

            _logger.LogInformation("Saved claim with ID: {Id}, Type: {Type}, Status: {Status}",
                claim.Id, claim.TypeOfReclamation, claim.Status);
            return CreatedAtAction(nameof(GetClaimById), new { id = claim.Id }, claim);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateClaim(int id, [FromBody] Claim claim)
        {
            if (claim == null)
            {
                _logger.LogWarning("Attempt to update claim with null data");
                return BadRequest("Claim data is missing.");
            }

            _logger.LogInformation("Updating claim with ID: {Id}", id);
            var updatedClaim = await _claimService.UpdateClaimAsync(id, claim);
            if (updatedClaim == null)
            {
                _logger.LogWarning("Claim with ID: {Id} not found for update", id);
                return NotFound();
            }

            _logger.LogInformation("Claim updated: {@Claim}", updatedClaim);
            return Ok(updatedClaim);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteClaim(int id)
        {
            await _claimService.DeleteClaimAsync(id);  // Just await the method without assigning its result
            return NoContent();
        }
    }
}